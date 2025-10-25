"""
Data fetcher module for CIA Factbook JSON to Excel Exporter.

Handles HTTP requests to GitHub raw content and JSON parsing.
"""

import json
import logging
import time
from typing import Dict, Optional, Tuple

import requests

from config import (
    URL_TEMPLATE, 
    REQUEST_TIMEOUT, 
    REQUEST_RETRY_DELAY
)
from config_loader import get_country_region, get_country_name, validate_country_code as validate_country_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """Handles fetching country data from the CIA Factbook GitHub repository."""
    
    def __init__(self):
        """Initialize the data fetcher."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CIA-Factbook-Exporter/1.0'
        })
    
    def construct_url(self, gec_code: str) -> Optional[str]:
        """
        Construct the GitHub raw content URL for a given country code.
        
        Args:
            gec_code: GEC country code (e.g., 'fr', 'gm')
            
        Returns:
            URL string or None if code is invalid
        """
        region = get_country_region(gec_code)
        if not region:
            logger.warning(f"Unknown country code: {gec_code}")
            return None
        
        url = URL_TEMPLATE.format(region=region, code=gec_code)
        return url
    
    def fetch_country_data(self, gec_code: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Fetch JSON data for a specific country.
        
        Args:
            gec_code: GEC country code
            
        Returns:
            Tuple of (parsed_json_data, error_message)
            If successful, error_message is None
            If failed, parsed_json_data is None
        """
        url = self.construct_url(gec_code)
        if not url:
            error_msg = f"Invalid country code: {gec_code}"
            logger.error(error_msg)
            return None, error_msg
        
        country_name = get_country_name(gec_code) or gec_code.upper()
        logger.info(f"Fetching data for {country_name} ({gec_code}) from: {url}")
        
        try:
            # Make HTTP request with timeout
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            # Parse JSON response
            json_data = response.json()
            logger.info(f"Successfully fetched data for {country_name}")
            return json_data, None
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error fetching {country_name} ({gec_code}): {str(e)}"
            logger.error(error_msg)
            return None, error_msg
            
        except json.JSONDecodeError as e:
            error_msg = f"JSON parsing error for {country_name} ({gec_code}): {str(e)}"
            logger.error(error_msg)
            return None, error_msg
            
        except Exception as e:
            error_msg = f"Unexpected error fetching {country_name} ({gec_code}): {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    def fetch_multiple_countries(self, gec_codes: list[str]) -> Dict[str, Tuple[Optional[Dict], Optional[str]]]:
        """
        Fetch data for multiple countries.
        
        Args:
            gec_codes: List of GEC country codes
            
        Returns:
            Dictionary mapping country codes to (data, error) tuples
        """
        results = {}
        
        for i, gec_code in enumerate(gec_codes):
            logger.info(f"Processing country {i+1}/{len(gec_codes)}: {gec_code}")
            
            data, error = self.fetch_country_data(gec_code)
            results[gec_code] = (data, error)
            
            # Add small delay between requests to be respectful to GitHub
            if i < len(gec_codes) - 1:
                time.sleep(REQUEST_RETRY_DELAY)
        
        return results
    
    def validate_country_code(self, gec_code: str) -> bool:
        """
        Validate if a country code is supported.
        
        Args:
            gec_code: GEC country code to validate
            
        Returns:
            True if code is valid, False otherwise
        """
        return validate_country_config(gec_code)
