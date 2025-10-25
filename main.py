"""
Main application module for CIA Factbook JSON to Excel Exporter.

Provides user interface and orchestrates the data fetching, parsing, and export process.
"""

import logging
import sys
from typing import List

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


class FactbookExporter:
    """Main application class for the CIA Factbook Exporter."""
    
    def __init__(self):
        """Initialize the application with all components."""
        self.fetcher = DataFetcher()
        self.parser = DataParser()
        self.exporter = ExcelExporter()
        
        logger.info("CIA Factbook Exporter initialized")
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        print("=" * 60)
        print("CIA Factbook JSON to Excel Exporter v1.0")
        print("=" * 60)
        print()
        print("This tool extracts country data from the CIA World Factbook")
        print("and exports selected fields to an Excel file.")
        print()
        print("Supported country codes (GEC format):")
        
        # Display available countries by region
        gec_to_name = get_all_countries()
        gec_to_region = get_all_regions()
        
        regions = {}
        for code, name in gec_to_name.items():
            region = gec_to_region.get(code, 'unknown')
            if region not in regions:
                regions[region] = []
            regions[region].append(f"{code} ({name})")
        
        for region, countries in sorted(regions.items()):
            print(f"\n{region.replace('-', ' ').title()}:")
            for country in sorted(countries):
                print(f"  • {country}")
        
        print("\n" + "=" * 60)
    
    def get_user_input(self) -> List[str]:
        """
        Get country codes from user input.
        
        Returns:
            List of validated country codes
        """
        while True:
            try:
                user_input = input(
                    "\nEnter country codes (comma-separated, e.g., fr,gm,au): "
                ).strip()
                
                if not user_input:
                    print("Error: Please enter at least one country code.")
                    continue
                
                # Parse and validate country codes
                codes = [code.strip().lower() for code in user_input.split(',')]
                valid_codes = []
                invalid_codes = []
                
                for code in codes:
                    if self.fetcher.validate_country_code(code):
                        valid_codes.append(code)
                    else:
                        invalid_codes.append(code)
                
                if invalid_codes:
                    print(f"\nWarning: Invalid country codes found: {', '.join(invalid_codes)}")
                    print(f"These will be skipped: {invalid_codes}")
                
                if not valid_codes:
                    print("Error: No valid country codes provided. Please try again.")
                    continue
                
                return valid_codes
                
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                sys.exit(0)
            except Exception as e:
                print(f"Error reading input: {str(e)}")
    
    def process_countries(self, country_codes: List[str]) -> bool:
        """
        Process the specified countries: fetch, parse, and export data.
        
        Args:
            country_codes: List of country codes to process
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\nProcessing {len(country_codes)} countries...")
        print("-" * 40)
        
        # Step 1: Fetch data from GitHub
        print("Step 1: Fetching data from CIA Factbook...")
        fetch_results = self.fetcher.fetch_multiple_countries(country_codes)
        
        # Count successful fetches
        successful_fetches = sum(1 for data, error in fetch_results.values() if data is not None)
        failed_fetches = len(country_codes) - successful_fetches
        
        print(f"Successfully fetched data for {successful_fetches} countries")
        if failed_fetches > 0:
            print(f"Failed to fetch data for {failed_fetches} countries")
        
        # Step 2: Parse the fetched data
        print("\nStep 2: Parsing extracted fields...")
        
        # Extract only the data (ignore errors) for parsing
        country_data = {code: data for code, (data, error) in fetch_results.items()}
        parsed_data = self.parser.parse_multiple_countries(country_data)
        
        print(f"Successfully parsed data for {len(parsed_data)} countries")
        
        # Show field summary
        field_summary = self.parser.get_field_summary(parsed_data)
        if field_summary:
            print("\nField availability summary:")
            for field_name, count in field_summary.items():
                print(f"  • {field_name}: {count}/{len(parsed_data)} countries")
        
        # Step 3: Export to Excel
        print("\nStep 3: Exporting to Excel...")
        export_path = self.exporter.export_to_excel(parsed_data)
        
        if export_path:
            print(f"✓ Success! Excel file created: {export_path}")
            
            # Show export summary
            summary = self.exporter.get_export_summary(parsed_data)
            print(f"\nExport Summary:")
            print(f"  • Countries processed: {summary['total_countries']}")
            print(f"  • Fields extracted: {summary['total_fields']}")
            print(f"  • Output file: {summary['output_file']}")
            
            # Show file size if available
            file_size = self.exporter.get_file_size()
            if file_size:
                print(f"  • File size: {file_size:,} bytes")
            
            return True
        else:
            print("✗ Failed to export data to Excel")
            return False
    
    def run(self):
        """Run the main application workflow."""
        try:
            # Display welcome message
            self.display_welcome()
            
            # Get user input
            country_codes = self.get_user_input()
            
            # Process the countries
            success = self.process_countries(country_codes)
            
            if success:
                print("\n" + "=" * 60)
                print("Export completed successfully!")
                print("=" * 60)
            else:
                print("\n" + "=" * 60)
                print("Export failed. Please check the error messages above.")
                print("=" * 60)
                sys.exit(1)
                
        except Exception as e:
            logger.error(f"Unexpected error in main application: {str(e)}")
            print(f"\nAn unexpected error occurred: {str(e)}")
            print("Please check the logs for more details.")
            sys.exit(1)


def main():
    """Main entry point for the application."""
    app = FactbookExporter()
    app.run()


if __name__ == "__main__":
    main()
