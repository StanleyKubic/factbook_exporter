#!/usr/bin/env python3
"""
Simplified Coverage Analysis Script for CIA Factbook

Generates simplified coverage report with field name, JSON path, and coverage percentage only.

Usage:
    python scripts/analyze_coverage_simple.py

Runtime: 5-10 minutes (fetches 260 country JSON files)
Frequency: One-time run, re-run only when Factbook structure changes
"""

import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import yaml
from tqdm import tqdm

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from fetcher import DataFetcher
from config_loader import load_countries

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimpleCoverageAnalyzer:
    """Analyzes field coverage across all CIA Factbook countries in simplified format."""
    
    def __init__(self):
        """Initialize the simplified coverage analyzer."""
        self.fetcher = DataFetcher()
        self.countries = load_countries()
        self.total_countries = len(self.countries)
        self.field_presence: Dict[str, int] = {}
        self.processed_countries = 0
        self.failed_countries = []
        
    def extract_leaf_field_paths(self, data: Dict, prefix: str = "") -> List[str]:
        """
        Recursively traverse JSON structure and collect all available leaf field paths.
        
        Args:
            data: JSON data dictionary
            prefix: Current field path prefix
            
        Returns:
            List of leaf field paths in dot notation
        """
        field_paths = []
        
        if not isinstance(data, dict):
            return field_paths
        
        for key, value in data.items():
            current_path = f"{prefix}.{key}" if prefix else key
            
            # Skip if key starts with underscore (likely metadata)
            if key.startswith('_'):
                continue
                
            if isinstance(value, dict):
                # Recurse into nested objects
                nested_paths = self.extract_leaf_field_paths(value, current_path)
                field_paths.extend(nested_paths)
            elif isinstance(value, list) and value:
                # Handle lists - check if it contains dictionaries
                first_item = value[0]
                if isinstance(first_item, dict):
                    # For lists of objects, process the first item as representative
                    nested_paths = self.extract_leaf_field_paths(first_item, current_path)
                    field_paths.extend(nested_paths)
                else:
                    # For lists of values, this is a leaf node
                    if self._has_meaningful_value(value):
                        field_paths.append(current_path)
            else:
                # This is a leaf node - check if it has a meaningful value
                if self._has_meaningful_value(value):
                    field_paths.append(current_path)
        
        return field_paths
    
    def _has_meaningful_value(self, value) -> bool:
        """
        Check if a value has meaningful content.
        
        Args:
            value: Value to check
            
        Returns:
            True if value is meaningful, False otherwise
        """
        if value is None:
            return False
        
        if isinstance(value, str):
            return value.strip() != ""
        
        if isinstance(value, list):
            return len(value) > 0
        
        return True
    
    def generate_field_name(self, json_path: str) -> str:
        """
        Generate field name from JSON path.
        Extract last segment of json_path without .text suffix.
        
        Args:
            json_path: Dot notation path (e.g., "Geography.Location.text")
            
        Returns:
            Field name (e.g., "Location")
        """
        # Remove .text suffix if present
        if json_path.endswith('.text'):
            json_path = json_path[:-5]
        
        # Extract last segment
        segments = json_path.split('.')
        field_name = segments[-1]
        
        # Convert from camelCase/PascalCase to readable format
        # Handle common abbreviations and special cases
        readable_name = self._make_readable(field_name)
        
        return readable_name
    
    def _make_readable(self, field_name: str) -> str:
        """
        Convert field name to readable format.
        
        Args:
            field_name: Raw field name
            
        Returns:
            Readable field name
        """
        # Handle special cases and abbreviations
        abbreviations = {
            'gdp': 'GDP',
            'gini': 'Gini',
            'hiv': 'HIV',
            'aids': 'AIDS',
            'co2': 'CO2',
            'pm25': 'PM2.5',
            'us': 'US',
            'uk': 'UK',
            'eu': 'EU',
            'un': 'UN',
            'nato': 'NATO',
            'wto': 'WTO',
            'imf': 'IMF',
            'worldbank': 'World Bank',
        }
        
        lower_name = field_name.lower()
        
        # Check for known abbreviations
        for abbr, full in abbreviations.items():
            if abbr in lower_name:
                field_name = field_name.replace(abbr, full, 1)
        
        # Insert spaces before capital letters (for camelCase)
        import re
        readable = re.sub(r'(?<!^)(?=[A-Z])', ' ', field_name)
        
        # Capitalize first letter of each word
        readable = ' '.join(word.capitalize() for word in readable.split())
        
        return readable
    
    def process_single_country(self, country: Dict) -> Tuple[Optional[List[str]], bool]:
        """
        Process a single country and extract its leaf field paths.
        
        Args:
            country: Country dictionary with code, name, region
            
        Returns:
            Tuple of (field_paths, success_flag)
        """
        country_code = country['code']
        country_name = country['name']
        
        try:
            # Fetch country data
            json_data, error = self.fetcher.fetch_country_data(country_code)
            
            if error:
                logger.error(f"Failed to fetch {country_name} ({country_code}): {error}")
                return None, False
            
            if not json_data:
                logger.warning(f"No data received for {country_name} ({country_code})")
                return None, False
            
            # Extract leaf field paths
            field_paths = self.extract_leaf_field_paths(json_data)
            logger.debug(f"Extracted {len(field_paths)} leaf fields for {country_name}")
            
            return field_paths, True
            
        except Exception as e:
            logger.error(f"Error processing {country_name} ({country_code}): {str(e)}")
            return None, False
    
    def analyze_all_countries(self) -> None:
        """Analyze field coverage across all countries."""
        logger.info(f"Starting simplified coverage analysis for {self.total_countries} countries")
        
        # Process countries with progress bar
        with tqdm(total=self.total_countries, desc="Analyzing countries", unit="country") as pbar:
            for country in self.countries:
                country_code = country['code']
                country_name = country['name']
                
                pbar.set_postfix_str(f"Processing {country_name}")
                
                field_paths, success = self.process_single_country(country)
                
                if success and field_paths:
                    # Track field presence across countries
                    for field_path in field_paths:
                        if field_path not in self.field_presence:
                            self.field_presence[field_path] = 0
                        self.field_presence[field_path] += 1
                    
                    self.processed_countries += 1
                else:
                    self.failed_countries.append(country_code)
                
                pbar.update(1)
        
        logger.info(f"Analysis complete. Processed: {self.processed_countries}, Failed: {len(self.failed_countries)}")
    
    def generate_simplified_report(self) -> Dict[str, Any]:
        """Generate the simplified coverage report."""
        logger.info("Generating simplified coverage report...")
        
        # Calculate coverage percentages and prepare field data
        fields_data = []
        
        for field_path, presence_count in self.field_presence.items():
            coverage_pct = (presence_count / self.processed_countries * 100) if self.processed_countries > 0 else 0.0
            field_name = self.generate_field_name(field_path)
            
            fields_data.append({
                'field_name': field_name,
                'json_path': field_path,
                'coverage_pct': round(coverage_pct, 1)
            })
        
        # Sort fields by coverage percentage descending
        fields_data.sort(key=lambda x: x['coverage_pct'], reverse=True)
        
        # Generate report
        report = {
            'metadata': {
                'total_countries': self.total_countries,
                'generated_at': self._get_timestamp()
            },
            'fields': fields_data
        }
        
        return report
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for report metadata."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_report(self, report: Dict[str, Any], output_path: str) -> None:
        """
        Save the simplified coverage report to a YAML file.
        
        Args:
            report: Coverage report dictionary
            output_path: Path to save the report
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(report, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
            logger.info(f"Simplified coverage report saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save report: {str(e)}")
            raise
    
    def run_analysis(self, output_path: str = "reports/coverage_simple.yaml") -> None:
        """
        Run the complete simplified coverage analysis.
        
        Args:
            output_path: Path to save the coverage report
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Run analysis
            self.analyze_all_countries()
            
            # Generate report
            report = self.generate_simplified_report()
            
            # Save report
            self.save_report(report, output_path)
            
            # Print summary
            self._print_summary(report)
            
        except KeyboardInterrupt:
            logger.info("Analysis interrupted by user")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            sys.exit(1)
    
    def _print_summary(self, report: Dict[str, Any]) -> None:
        """Print a summary of the simplified coverage analysis."""
        metadata = report["metadata"]
        fields = report["fields"]
        
        print("\n" + "="*60)
        print("SIMPLIFIED COVERAGE ANALYSIS SUMMARY")
        print("="*60)
        print(f"Total countries: {metadata['total_countries']}")
        print(f"Successfully processed: {self.processed_countries}")
        print(f"Failed: {len(self.failed_countries)}")
        print(f"Total unique fields: {len(fields)}")
        print()
        print("Top 15 most covered fields:")
        
        # Show top 15 fields by coverage
        for i, field_data in enumerate(fields[:15], 1):
            print(f"  {i:2d}. {field_data['coverage_pct']:5.1f}% - {field_data['field_name']}")
            print(f"      Path: {field_data['json_path']}")
        
        print()
        print("Bottom 10 least covered fields:")
        
        # Show bottom 10 fields by coverage
        for i, field_data in enumerate(fields[-10:], len(fields) - 9):
            print(f"  {i:2d}. {field_data['coverage_pct']:5.1f}% - {field_data['field_name']}")
            print(f"      Path: {field_data['json_path']}")
        
        print()
        print(f"Full report saved to: reports/coverage_simple.yaml")
        print("="*60)


def main():
    """Main entry point for the simplified coverage analysis script."""
    print("CIA Factbook Simplified Coverage Analysis")
    print("Generating simplified coverage report with field name, JSON path, and coverage percentage...")
    print()
    
    analyzer = SimpleCoverageAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
