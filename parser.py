"""
Data parser module for CIA Factbook JSON to Excel Exporter.

Handles extraction of specific fields from nested JSON structure.
"""

import logging
from typing import Any, Dict, Optional

from config_loader import get_all_field_mappings, get_country_name
from cleaner import clean_value

# Configure logging
logger = logging.getLogger(__name__)


class DataParser:
    """Handles parsing and extracting data from CIA Factbook JSON structure."""
    
    def __init__(self):
        """Initialize data parser."""
        self.section_definitions = get_all_field_mappings()
    
    def get_nested_value(self, data: Dict, path: str) -> Optional[Any]:
        """
        Extract a value from a nested dictionary using dot notation path.
        
        Args:
            data: The nested dictionary to navigate
            path: Dot-separated path (e.g., "Geography.Location")
            
        Returns:
            The extracted value or None if path doesn't exist
        """
        try:
            keys = path.split('.')
            current = data
            
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    logger.debug(f"Path not found: {path}")
                    return None
            
            return current
            
        except Exception as e:
            logger.warning(f"Error navigating path '{path}': {str(e)}")
            return None
    
    def extract_text_value(self, value: Any) -> Optional[str]:
        """
        Extract clean text value from various data types with HTML cleaning.
        
        Args:
            value: The raw value from JSON
            
        Returns:
            Cleaned string value or None
        """
        if value is None:
            return None
        
        # Handle different data types
        if isinstance(value, str):
            # Apply HTML cleaning to string values
            return clean_value(value)
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, dict):
            # Some fields might be objects with a 'text' or similar field
            if 'text' in value:
                return clean_value(str(value['text']))
            elif 'value' in value:
                return clean_value(str(value['value']))
            else:
                # Convert dict to string representation and clean
                return clean_value(str(value))
        elif isinstance(value, list):
            # Join list elements with commas and clean each item
            if value:
                clean_items = [clean_value(str(item)) for item in value]
                return ', '.join(clean_items)
            else:
                return None
        else:
            return clean_value(str(value))
    
    def parse_country_data(self, gec_code: str, json_data: Dict) -> Dict[str, Optional[str]]:
        """
        Parse country JSON data and extract all configured fields.
        
        Args:
            gec_code: GEC country code
            json_data: Raw JSON data from CIA Factbook
            
        Returns:
            Dictionary with extracted field values
        """
        country_name = get_country_name(gec_code)
        if not country_name:
            country_name = gec_code.upper()
        
        logger.info(f"Parsing data for {country_name} ({gec_code})")
        
        # Initialize result with basic country info
        result = {
            'Country Code': gec_code.upper(),
            'Country Name': country_name
        }
        
        # Extract each configured field
        for json_path, column_name in self.section_definitions.items():
            raw_value = self.get_nested_value(json_data, json_path)
            clean_value = self.extract_text_value(raw_value)
            
            result[column_name] = clean_value
            
            if clean_value is not None:
                logger.debug(f"Extracted {column_name}: {clean_value[:50]}...")
            else:
                logger.debug(f"Field not found or empty: {json_path}")
        
        return result
    
    def parse_multiple_countries(self, country_data: Dict[str, Optional[Dict]]) -> Dict[str, Dict[str, Optional[str]]]:
        """
        Parse data for multiple countries.
        
        Args:
            country_data: Dictionary mapping country codes to JSON data
            
        Returns:
            Dictionary mapping country codes to parsed field data
        """
        results = {}
        
        for gec_code, json_data in country_data.items():
            if json_data is not None:
                try:
                    parsed_data = self.parse_country_data(gec_code, json_data)
                    results[gec_code] = parsed_data
                except Exception as e:
                    logger.error(f"Error parsing data for {gec_code}: {str(e)}")
                    # Add empty record with just basic info
                    country_name = get_country_name(gec_code)
                    if not country_name:
                        country_name = gec_code.upper()
                    results[gec_code] = {
                        'Country Code': gec_code.upper(),
                        'Country Name': country_name
                    }
            else:
                logger.warning(f"No data to parse for {gec_code}")
        
        return results
    
    def get_field_summary(self, parsed_data: Dict[str, Dict[str, Optional[str]]]) -> Dict[str, int]:
        """
        Get a summary of field availability across all countries.
        
        Args:
            parsed_data: Parsed data for multiple countries
            
        Returns:
            Dictionary mapping field names to count of non-null values
        """
        if not parsed_data:
            return {}
        
        # Get all field names from the first country
        first_country = next(iter(parsed_data.values()))
        field_names = first_country.keys()
        
        summary = {}
        for field_name in field_names:
            count = sum(1 for country_data in parsed_data.values() 
                       if country_data.get(field_name) is not None)
            summary[field_name] = count
        
        return summary
