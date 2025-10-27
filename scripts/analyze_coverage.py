#!/usr/bin/env python3
"""
Coverage Analysis Script for CIA Factbook

Analyzes field availability across all countries to determine which fields 
are universally present vs. partially available.

Usage:
    python scripts/analyze_coverage.py

Runtime: 5-10 minutes (fetches 260 country JSON files)
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

from src.core.fetcher import DataFetcher
from src.config.config_loader import load_countries, get_country_name, get_country_region

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CoverageAnalyzer:
    """Analyzes field coverage across all CIA Factbook countries."""
    
    def __init__(self):
        """Initialize the coverage analyzer."""
        self.fetcher = DataFetcher()
        self.countries = load_countries()
        self.total_countries = len(self.countries)
        self.field_coverage: Dict[str, Dict[str, Any]] = {}
        self.processed_countries = 0
        self.failed_countries = []
        
    def extract_field_paths(self, data: Dict, prefix: str = "") -> List[str]:
        """
        Recursively traverse JSON structure and collect all available field paths.
        
        Args:
            data: JSON data dictionary
            prefix: Current field path prefix
            
        Returns:
            List of field paths in dot notation
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
                nested_paths = self.extract_field_paths(value, current_path)
                field_paths.extend(nested_paths)
            elif isinstance(value, list) and value:
                # Handle lists - check if it contains dictionaries
                first_item = value[0]
                if isinstance(first_item, dict):
                    # For lists of objects, process the first item as representative
                    nested_paths = self.extract_field_paths(first_item, current_path)
                    field_paths.extend(nested_paths)
                else:
                    # For lists of values, this is a leaf node
                    if value and str(value).strip():
                        field_paths.append(current_path)
            else:
                # This is a leaf node - check if it has a meaningful value
                if value is not None and str(value).strip():
                    field_paths.append(current_path)
        
        return field_paths
    
    def classify_field_tier(self, coverage_pct: float) -> str:
        """
        Classify a field based on its coverage percentage.
        
        Args:
            coverage_pct: Coverage percentage (0-100)
            
        Returns:
            Tier classification: "universal", "common", or "partial"
        """
        if coverage_pct >= 95.0:
            return "universal"
        elif coverage_pct >= 70.0:
            return "common"
        else:
            return "partial"
    
    def update_field_coverage(self, field_paths: List[str], country_code: str) -> None:
        """
        Update coverage statistics for a set of field paths.
        
        Args:
            field_paths: List of field paths found in the country
            country_code: Country GEC code
        """
        # Get all unique field paths seen so far
        all_fields = set(self.field_coverage.keys())
        all_fields.update(field_paths)
        
        # Initialize new fields
        for field in all_fields:
            if field not in self.field_coverage:
                self.field_coverage[field] = {
                    "present": 0,
                    "missing": 0,
                    "missing_countries": []
                }
        
        # Update coverage for each field
        for field in all_fields:
            if field in field_paths:
                self.field_coverage[field]["present"] += 1
            else:
                self.field_coverage[field]["missing"] += 1
                self.field_coverage[field]["missing_countries"].append(country_code)
    
    def process_single_country(self, country: Dict) -> Tuple[Optional[List[str]], bool]:
        """
        Process a single country and extract its field paths.
        
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
            
            # Extract field paths
            field_paths = self.extract_field_paths(json_data)
            logger.debug(f"Extracted {len(field_paths)} fields for {country_name}")
            
            return field_paths, True
            
        except Exception as e:
            logger.error(f"Error processing {country_name} ({country_code}): {str(e)}")
            return None, False
    
    def analyze_all_countries(self) -> None:
        """Analyze field coverage across all countries."""
        logger.info(f"Starting coverage analysis for {self.total_countries} countries")
        
        # Process countries with progress bar
        with tqdm(total=self.total_countries, desc="Analyzing countries", unit="country") as pbar:
            for country in self.countries:
                country_code = country['code']
                country_name = country['name']
                
                pbar.set_postfix_str(f"Processing {country_name}")
                
                field_paths, success = self.process_single_country(country)
                
                if success and field_paths:
                    self.update_field_coverage(field_paths, country_code)
                    self.processed_countries += 1
                else:
                    self.failed_countries.append(country_code)
                
                pbar.update(1)
        
        logger.info(f"Analysis complete. Processed: {self.processed_countries}, Failed: {len(self.failed_countries)}")
    
    def calculate_coverage_stats(self) -> None:
        """Calculate final coverage statistics and classifications for all fields."""
        logger.info("Calculating coverage statistics...")
        
        for field, stats in self.field_coverage.items():
            # Calculate coverage percentage
            total = stats["present"] + stats["missing"]
            coverage_pct = (stats["present"] / total * 100) if total > 0 else 0.0
            
            # Update stats
            stats["coverage_pct"] = round(coverage_pct, 1)
            stats["tier"] = self.classify_field_tier(coverage_pct)
    
    def generate_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics for the report."""
        total_fields = len(self.field_coverage)
        universal_fields = sum(1 for stats in self.field_coverage.values() if stats["tier"] == "universal")
        common_fields = sum(1 for stats in self.field_coverage.values() if stats["tier"] == "common")
        partial_fields = sum(1 for stats in self.field_coverage.values() if stats["tier"] == "partial")
        
        return {
            "total_countries": self.total_countries,
            "processed_countries": self.processed_countries,
            "failed_countries": len(self.failed_countries),
            "total_unique_fields": total_fields,
            "universal_fields": universal_fields,
            "common_fields": common_fields,
            "partial_fields": partial_fields
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate the complete coverage report."""
        logger.info("Generating coverage report...")
        
        # Calculate coverage statistics
        self.calculate_coverage_stats()
        
        # Sort fields by coverage percentage (descending)
        sorted_fields = dict(
            sorted(
                self.field_coverage.items(),
                key=lambda x: x[1]["coverage_pct"],
                reverse=True
            )
        )
        
        # Generate report
        report = {
            "metadata": {
                "generated_at": self._get_timestamp(),
                "script_version": "1.0",
                "total_countries_analyzed": self.total_countries
            },
            "fields": sorted_fields,
            "summary": self.generate_summary_stats()
        }
        
        # Add failed countries if any
        if self.failed_countries:
            report["failed_countries"] = {
                "count": len(self.failed_countries),
                "codes": sorted(self.failed_countries)
            }
        
        return report
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for report metadata."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_report(self, report: Dict[str, Any], output_path: str) -> None:
        """
        Save the coverage report to a YAML file.
        
        Args:
            report: Coverage report dictionary
            output_path: Path to save the report
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(report, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
            logger.info(f"Coverage report saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save report: {str(e)}")
            raise
    
    def run_analysis(self, output_path: str = "reports/coverage_report.yaml") -> None:
        """
        Run the complete coverage analysis.
        
        Args:
            output_path: Path to save the coverage report
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Run analysis
            self.analyze_all_countries()
            
            # Generate report
            report = self.generate_report()
            
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
        """Print a summary of the coverage analysis."""
        summary = report["summary"]
        
        print("\n" + "="*60)
        print("COVERAGE ANALYSIS SUMMARY")
        print("="*60)
        print(f"Total countries: {summary['total_countries']}")
        print(f"Successfully processed: {summary['processed_countries']}")
        print(f"Failed: {summary['failed_countries']}")
        print(f"Total unique fields: {summary['total_unique_fields']}")
        print()
        print("Field distribution by tier:")
        print(f"  Universal (≥95%): {summary['universal_fields']} fields")
        print(f"  Common (70-94%):   {summary['common_fields']} fields")
        print(f"  Partial (<70%):    {summary['partial_fields']} fields")
        print()
        print("Top 10 most covered fields:")
        
        # Show top 10 fields by coverage
        fields = list(report["fields"].items())[:10]
        for field_path, stats in fields:
            print(f"  {stats['coverage_pct']:5.1f}% - {field_path}")
        
        print()
        print(f"Full report saved to: reports/coverage_report.yaml")
        print("="*60)


def main():
    """Main entry point for the coverage analysis script."""
    print("CIA Factbook Coverage Analysis")
    print("Analyzing field availability across all countries...")
    print()
    
    analyzer = CoverageAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
