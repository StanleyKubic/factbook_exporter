#!/usr/bin/env python3
"""
Country configuration generator for CIA Factbook JSON to Excel Exporter.

This script fetches country data from the CIA Factbook GitHub repository
and generates a static YAML configuration file with all country mappings.
"""

import json
import os
import sys
from typing import Dict, List, Optional
import yaml
import requests
from pathlib import Path


class CountryDataGenerator:
    """Generates country configuration data from CIA Factbook repository."""
    
    def __init__(self):
        """Initialize the generator."""
        self.base_url = "https://github.com/factbook/factbook.json/raw/master"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CIA-Factbook-Exporter/1.0'
        })
        
    def get_available_regions(self) -> List[str]:
        """
        Get list of available regions from the repository.
        
        Returns:
            List of region names
        """
        # Common regions based on the current hardcoded mappings
        # and typical CIA Factbook structure
        regions = [
            "africa",
            "australia-oceania", 
            "central-asia",
            "east-n-southeast-asia",
            "europe",
            "middle-east",
            "north-america",
            "south-america",
            "south-asia"
        ]
        return regions
    
    def fetch_region_index(self, region: str) -> Optional[Dict]:
        """
        Fetch the index file for a region to get available countries.
        
        Args:
            region: Region name
            
        Returns:
            Dictionary with country information or None if failed
        """
        url = f"{self.base_url}/{region}/index.json"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Warning: Could not fetch index for {region}: {e}")
            return None
    
    def extract_country_from_index(self, index_data: Dict) -> List[Dict]:
        """
        Extract country information from region index data.
        
        Args:
            index_data: Region index JSON data
            
        Returns:
            List of country dictionaries
        """
        countries = []
        
        # The index structure might vary, so we'll try different approaches
        if isinstance(index_data, dict):
            # Look for country entries in various possible structures
            for key, value in index_data.items():
                if isinstance(value, dict) and 'gec' in value:
                    # Found a country entry with GEC code
                    countries.append({
                        'code': value.get('gec', '').lower(),
                        'name': value.get('name', key),
                        'region': value.get('region', '')
                    })
                elif isinstance(value, dict) and 'name' in value:
                    # Alternative structure
                    code = key.lower() if len(key) == 2 else ''
                    if code:
                        countries.append({
                            'code': code,
                            'name': value.get('name', key),
                            'region': ''
                        })
        
        return countries
    
    def get_countries_from_current_config(self) -> List[Dict]:
        """
        Get countries from the current hardcoded configuration as fallback.
        
        Returns:
            List of country dictionaries from current config
        """
        # Import current config as fallback
        sys.path.append(str(Path(__file__).parent.parent))
        try:
            from config import GEC_TO_REGION, GEC_TO_NAME
            
            countries = []
            for code in GEC_TO_NAME:
                countries.append({
                    'code': code,
                    'name': GEC_TO_NAME[code],
                    'region': GEC_TO_REGION.get(code, '')
                })
            
            return sorted(countries, key=lambda x: x['code'])
        except ImportError:
            return []
    
    def fetch_all_countries(self) -> List[Dict]:
        """
        Fetch all available countries from the repository.
        
        Returns:
            List of all country dictionaries
        """
        all_countries = []
        regions = self.get_available_regions()
        
        print("Fetching country data from CIA Factbook repository...")
        
        for region in regions:
            print(f"  Processing region: {region}")
            
            index_data = self.fetch_region_index(region)
            if index_data:
                region_countries = self.extract_country_from_index(index_data)
                
                # Add region info to countries
                for country in region_countries:
                    country['region'] = region
                
                all_countries.extend(region_countries)
                print(f"    Found {len(region_countries)} countries")
            else:
                print(f"    Could not fetch data for {region}")
        
        # If we couldn't fetch from repository, use current config as fallback
        if not all_countries:
            print("Warning: Could not fetch from repository, using current config as fallback")
            all_countries = self.get_countries_from_current_config()
        
        # Remove duplicates and sort
        seen_codes = set()
        unique_countries = []
        
        for country in all_countries:
            code = country['code']
            if code and code not in seen_codes:
                seen_codes.add(code)
                unique_countries.append(country)
        
        return sorted(unique_countries, key=lambda x: x['code'])
    
    def generate_yaml_config(self, countries: List[Dict], output_path: str) -> bool:
        """
        Generate YAML configuration file from country data.
        
        Args:
            countries: List of country dictionaries
            output_path: Path to output YAML file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Structure the data for YAML
            config_data = {
                'countries': countries
            }
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write YAML file
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, 
                         sort_keys=False, allow_unicode=True, indent=2)
            
            print(f"Generated YAML configuration with {len(countries)} countries")
            print(f"Output file: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"Error generating YAML config: {e}")
            return False
    
    def run(self, output_path: str = "config/countries.yaml") -> bool:
        """
        Run the complete generation process.
        
        Args:
            output_path: Path for the output YAML file
            
        Returns:
            True if successful, False otherwise
        """
        print("=" * 60)
        print("CIA Factbook Country Configuration Generator")
        print("=" * 60)
        print()
        
        # Fetch all countries
        countries = self.fetch_all_countries()
        
        if not countries:
            print("Error: No countries found")
            return False
        
        print(f"\nTotal countries found: {len(countries)}")
        print("\nSample countries:")
        for i, country in enumerate(countries[:5]):
            print(f"  • {country['code'].upper()}: {country['name']} ({country['region']})")
        
        if len(countries) > 5:
            print(f"  ... and {len(countries) - 5} more")
        
        print()
        
        # Generate YAML configuration
        success = self.generate_yaml_config(countries, output_path)
        
        if success:
            print("\n" + "=" * 60)
            print("Generation completed successfully!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("Generation failed!")
            print("=" * 60)
        
        return success


def main():
    """Main entry point for the generation script."""
    generator = CountryDataGenerator()
    
    # Get output path from command line args or use default
    output_path = sys.argv[1] if len(sys.argv) > 1 else "config/countries.yaml"
    
    success = generator.run(output_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
