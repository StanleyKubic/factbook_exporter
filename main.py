"""
Main application module for CIA Factbook JSON to Excel Exporter.

Provides CLI interface using Click for professional argument parsing
and orchestrates the data fetching, parsing, and export process.
"""

import logging
import sys
from typing import List

import click
from config_loader import get_all_countries, get_all_regions
from fetcher import DataFetcher
from parser import DataParser
from exporter import ExcelExporter

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
def main(countries, output, interactive, verbose):
    """CIA Factbook Data Exporter - Extract country data to Excel"""
    
    # Interactive mode
    if interactive:
        click.echo("CIA Factbook JSON to Excel Exporter v1.3")
        click.echo("=" * 50)
        
        # Display available countries
        gec_to_name = get_all_countries()
        gec_to_region = get_all_regions()
        
        regions = {}
        for code, name in gec_to_name.items():
            region = gec_to_region.get(code, 'unknown')
            if region not in regions:
                regions[region] = []
            regions[region].append(f"{code} ({name})")
        
        click.echo("\nAvailable countries by region:")
        for region, countries_list in sorted(regions.items()):
            click.echo(f"\n{region.replace('-', ' ').title()}:")
            for country in sorted(countries_list):
                click.echo(f"  • {country}")
        
        countries = click.prompt('\nEnter country codes (comma-separated)', type=str)
        output = click.prompt('Output filename', default='countries_data.xlsx')
    
    # Validate that countries were provided
    if not countries:
        click.echo('Error: Please provide country codes via --countries or use --interactive', err=True)
        click.echo('Run with --help for usage information')
        sys.exit(1)
    
    # Parse comma-separated codes
    country_list = [code.strip().lower() for code in countries.split(',')]
    
    if verbose:
        click.echo(f'Processing {len(country_list)} countries: {", ".join(country_list)}')
    
    # Initialize components
    fetcher = DataFetcher()
    parser = DataParser()
    exporter = ExcelExporter()
    
    try:
        # Step 1: Fetch data from GitHub
        if verbose:
            click.echo("Step 1: Fetching data from CIA Factbook...")
        
        fetch_results = fetcher.fetch_multiple_countries(country_list)
        
        # Count successful fetches
        successful_fetches = sum(1 for data, error in fetch_results.values() if data is not None)
        failed_fetches = len(country_list) - successful_fetches
        
        if verbose:
            click.echo(f"Successfully fetched data for {successful_fetches} countries")
            if failed_fetches > 0:
                click.echo(f"Failed to fetch data for {failed_fetches} countries")
        
        # Step 2: Parse the fetched data
        if verbose:
            click.echo("Step 2: Parsing extracted fields...")
        
        # Extract only the data (ignore errors) for parsing
        country_data = {code: data for code, (data, error) in fetch_results.items()}
        parsed_data = parser.parse_multiple_countries(country_data)
        
        if verbose:
            click.echo(f"Successfully parsed data for {len(parsed_data)} countries")
            
            # Show field summary
            field_summary = parser.get_field_summary(parsed_data)
            if field_summary:
                click.echo("\nField availability summary:")
                for field_name, count in field_summary.items():
                    click.echo(f"  • {field_name}: {count}/{len(parsed_data)} countries")
        
        # Step 3: Export to Excel
        if verbose:
            click.echo("Step 3: Exporting to Excel...")
        
        # Set custom output filename if provided
        if output != 'countries_data.xlsx':
            exporter.output_filename = output
            exporter._get_output_path = lambda: exporter.output_dir / output
        
        export_path = exporter.export_to_excel(parsed_data)
        
        if export_path:
            click.echo(f"✓ Success! Excel file created: {export_path}")
            
            # Show export summary
            summary = exporter.get_export_summary(parsed_data)
            click.echo(f"\nExport Summary:")
            click.echo(f"  • Countries processed: {summary['total_countries']}")
            click.echo(f"  • Fields extracted: {summary['total_fields']}")
            click.echo(f"  • Output file: {summary['output_file']}")
            
            # Show file size if available
            file_size = exporter.get_file_size()
            if file_size:
                click.echo(f"  • File size: {file_size:,} bytes")
        else:
            click.echo("✗ Failed to export data to Excel", err=True)
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error in main application: {str(e)}")
        click.echo(f"\nAn unexpected error occurred: {str(e)}", err=True)
        click.echo("Please check the logs for more details.", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
