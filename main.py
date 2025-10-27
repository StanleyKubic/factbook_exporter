"""
Main application module for CIA Factbook JSON to Excel Exporter.

Provides CLI interface using Click for professional argument parsing
and orchestrates the data fetching, parsing, and export process.
"""

import logging
import sys
from typing import List

import click
from src.config.config_loader import (
    get_all_countries, 
    get_all_regions, 
    get_profile_fields, 
    get_default_profile,
    list_available_profiles
)
from src.utils.validator import validate_country_codes, get_country_name
from src.core.fetcher import DataFetcher
from src.core.parser import DataParser
from src.core.exporter import ExcelExporter
from src.utils.ui_helpers import (
    console, 
    print_success, 
    print_error, 
    print_warning, 
    print_info,
    create_progress_bar
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--countries', '-c',
              help='Comma-separated country codes (e.g., fr,gm,uk)')
@click.option('--output', '-o',
              default='countries_data.xlsx',
              help='Output Excel filename')
@click.option('--interactive', '-i',
              is_flag=True,
              help='Interactive mode with prompts')
@click.option('--verbose', '-v',
              is_flag=True,
              help='Verbose output')
@click.option('--profile', '-p',
              default=None,
              help='Field selection profile (minimal, standard, geography, economy, comprehensive)')
@click.option('--list-profiles',
              is_flag=True,
              help='List available field profiles and exit')
def main(countries, output, interactive, verbose, profile, list_profiles):
    """CIA Factbook Data Exporter - Extract country data to Excel"""
    
    # Handle --list-profiles
    if list_profiles:
        profiles = list_available_profiles()
        print_info("Available field profiles:")
        for name, description in profiles.items():
            console.print(f"  [bold]{name}[/bold]: {description}")
        return
    
    # Interactive mode
    if interactive:
        console.print("CIA Factbook JSON to Excel Exporter v1.3", style="bold blue")
        console.print("=" * 50, style="blue")
        
        # Display available countries
        gec_to_name = get_all_countries()
        gec_to_region = get_all_regions()
        
        regions = {}
        for code, name in gec_to_name.items():
            region = gec_to_region.get(code, 'unknown')
            if region not in regions:
                regions[region] = []
            regions[region].append(f"{code} ({name})")
        
        console.print("\nAvailable countries by region:", style="cyan")
        for region, countries_list in sorted(regions.items()):
            console.print(f"\n{region.replace('-', ' ').title()}:", style="bold cyan")
            for country in sorted(countries_list):
                console.print(f"  • {country}", style="white")
        
        countries = click.prompt('\nEnter country codes (comma-separated)', type=str)
        output = click.prompt('Output filename', default='countries_data.xlsx')
    
    # Validate that countries were provided
    if not countries:
        print_error('Please provide country codes via --countries or use --interactive')
        print_info('Run with --help for usage information')
        sys.exit(1)
    
    # Parse comma-separated codes
    country_list = [code.strip().lower() for code in countries.split(',')]
    
    # Validate country codes
    print_info(f'Validating {len(country_list)} country codes...')
    
    valid_codes, invalid_codes = validate_country_codes(country_list)
    
    # Report invalid codes
    if invalid_codes:
        print_error(f'Invalid country codes: {", ".join(invalid_codes)}')
        print_warning(f'Tip: Country codes must exist in config/countries.yaml')
        print_warning(f'Run with --help or check the config file for valid codes')
        
        # Exit if no valid codes
        if not valid_codes:
            return
    
    # Report valid codes
    print_success(f'Valid codes: {len(valid_codes)} countries')
    
    if verbose:
        for code in valid_codes:
            name = get_country_name(code)
            console.print(f"  - {code}: {name}", style="white")
    
    if verbose:
        print_info(f'Processing {len(valid_codes)} countries: {", ".join(valid_codes)}')
    
    # Determine which profile to use
    if profile is None:
        profile = get_default_profile()
        if verbose:
            print_info(f"Using default profile: {profile}")
    else:
        if verbose:
            print_info(f"Using profile: {profile}")
    
    # Load fields from profile
    try:
        field_paths = get_profile_fields(profile)
        if verbose:
            print_info(f"Profile contains {len(field_paths)} fields")
    except ValueError as e:
        print_error(str(e))
        print_info("Run with --list-profiles to see available profiles")
        return
    
    # Convert field paths to field configs for parser
    fields_config = []
    for path in field_paths:
        # Extract column name from path (last segment before .text)
        if path.endswith('.text'):
            column_name = path.split('.')[-2]
        else:
            column_name = path.split('.')[-1]
        fields_config.append({
            'json_path': path,
            'column_name': column_name,
            'optional': False  # Profile fields are expected to exist
        })
    
    # Update country_list to use only valid codes
    country_list = valid_codes
    
    # Initialize components
    fetcher = DataFetcher()
    parser = DataParser()
    exporter = ExcelExporter()
    
    # Override parser's field mappings with profile fields
    parser.section_definitions = {field['json_path']: field['column_name'] for field in fields_config}
    
    try:
        # Step 1: Fetch data from GitHub
        print_info(f'Fetching data for {len(valid_codes)} countries...')
        
        # Create progress bar for fetching
        with create_progress_bar(len(valid_codes), "Fetching countries") as pbar:
            fetch_results = {}
            failed_countries = []
            
            for i, code in enumerate(valid_codes):
                try:
                    # Fetch individual country data
                    data, error = fetcher.fetch_country_data(code)
                    fetch_results[code] = (data, error)
                    
                    if error:
                        failed_countries.append(code)
                        print_warning(f"Failed to fetch {code}: {error}")
                    
                except Exception as e:
                    fetch_results[code] = (None, str(e))
                    failed_countries.append(code)
                    print_warning(f"Failed to fetch {code}: {str(e)}")
                
                pbar.update(1)
                
                # Add small delay between requests to be respectful to GitHub
                if i < len(valid_codes) - 1:
                    import time
                    time.sleep(0.5)  # Consistent with REQUEST_RETRY_DELAY
        
        # Count successful fetches
        successful_fetches = sum(1 for data, error in fetch_results.values() if data is not None)
        failed_fetches = len(valid_codes) - successful_fetches
        
        if successful_fetches > 0:
            print_success(f'Successfully fetched {successful_fetches}/{len(valid_codes)} countries')
        else:
            print_error('No countries successfully fetched. Export aborted.')
            return
        
        if failed_countries:
            print_warning(f'Failed countries: {", ".join(failed_countries)}')
        
        # Step 2: Parse the fetched data
        if verbose:
            print_info("Step 2: Parsing extracted fields...")
        
        # Extract only the data (ignore errors) for parsing
        country_data = {code: data for code, (data, error) in fetch_results.items() if data is not None}
        parsed_data = parser.parse_multiple_countries(country_data)
        
        if verbose:
            print_success(f"Successfully parsed data for {len(parsed_data)} countries")
            
            # Show field summary
            field_summary = parser.get_field_summary(parsed_data)
            if field_summary:
                console.print("\nField availability summary:", style="cyan")
                for field_name, count in field_summary.items():
                    console.print(f"  • {field_name}: {count}/{len(parsed_data)} countries", style="white")
        
        # Step 3: Export to Excel
        if verbose:
            print_info("Step 3: Exporting to Excel...")
        
        # Set custom output filename if provided
        if output != 'countries_data.xlsx':
            exporter.output_filename = output
            exporter._get_output_path = lambda: exporter.output_dir / output
        
        export_path = exporter.export_to_excel(parsed_data)
        
        if export_path:
            print_success(f'Export completed: {export_path}')
            
            # Show export summary
            summary = exporter.get_export_summary(parsed_data)
            console.print("\nExport Summary:", style="bold green")
            console.print(f"  • Countries processed: {summary['total_countries']}", style="white")
            console.print(f"  • Fields extracted: {summary['total_fields']}", style="white")
            console.print(f"  • Output file: {summary['output_file']}", style="white")
            
            # Show file size if available
            file_size = exporter.get_file_size()
            if file_size:
                console.print(f"  • File size: {file_size:,} bytes", style="white")
        else:
            print_error("Failed to export data to Excel")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error in main application: {str(e)}")
        print_error(f"An unexpected error occurred: {str(e)}")
        print_info("Please check the logs for more details.")
        sys.exit(1)


if __name__ == '__main__':
    main()
