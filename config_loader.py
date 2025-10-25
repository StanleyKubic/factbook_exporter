"""
Configuration loader module for CIA Factbook JSON to Excel Exporter.

Handles loading and parsing of YAML configuration files, providing
access to country mappings and other configuration data.
"""

import logging
import os
from typing import Dict, List, Optional
import yaml
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigLoader:
    """Handles loading and accessing configuration data from YAML files."""
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize the configuration loader.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self._countries_data: Optional[Dict] = None
        self._gec_to_name: Dict[str, str] = {}
        self._gec_to_region: Dict[str, str] = {}
        
        # Load configuration on initialization
        self._load_countries_config()
    
    def _load_countries_config(self) -> None:
        """Load countries configuration from YAML file."""
        countries_file = self.config_dir / "countries.yaml"
        
        if not countries_file.exists():
            raise FileNotFoundError(f"Countries configuration file not found: {countries_file}")
        
        try:
            with open(countries_file, 'r', encoding='utf-8') as f:
                self._countries_data = yaml.safe_load(f)
            
            if not self._countries_data or 'countries' not in self._countries_data:
                raise ValueError("Invalid countries configuration: missing 'countries' section")
            
            # Build lookup dictionaries for efficient access
            countries = self._countries_data['countries']
            
            for country in countries:
                code = country.get('code', '').lower()
                name = country.get('name', '')
                region = country.get('region', '')
                
                if code and name:
                    self._gec_to_name[code] = name
                    if region:
                        self._gec_to_region[code] = region
            
            logger.info(f"Loaded {len(self._gec_to_name)} countries from configuration")
            
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing countries configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading countries configuration: {e}")
    
    def load_countries(self) -> List[Dict]:
        """
        Load the complete countries list from configuration.
        
        Returns:
            List of country dictionaries with code, name, and region
        """
        if not self._countries_data:
            raise RuntimeError("Configuration not loaded")
        
        return self._countries_data.get('countries', [])
    
    def get_country_name(self, gec_code: str) -> Optional[str]:
        """
        Get the country name for a given GEC code.
        
        Args:
            gec_code: GEC country code (e.g., 'fr', 'gm')
            
        Returns:
            Country name or None if code not found
        """
        return self._gec_to_name.get(gec_code.lower())
    
    def get_country_region(self, gec_code: str) -> Optional[str]:
        """
        Get the region for a given GEC code.
        
        Args:
            gec_code: GEC country code (e.g., 'fr', 'gm')
            
        Returns:
            Region name or None if code not found
        """
        return self._gec_to_region.get(gec_code.lower())
    
    def get_all_countries(self) -> Dict[str, str]:
        """
        Get all country code to name mappings.
        
        Returns:
            Dictionary mapping GEC codes to country names
        """
        return self._gec_to_name.copy()
    
    def get_all_regions(self) -> Dict[str, str]:
        """
        Get all country code to region mappings.
        
        Returns:
            Dictionary mapping GEC codes to regions
        """
        return self._gec_to_region.copy()
    
    def validate_country_code(self, gec_code: str) -> bool:
        """
        Validate if a country code is supported.
        
        Args:
            gec_code: GEC country code to validate
            
        Returns:
            True if code is valid, False otherwise
        """
        return gec_code.lower() in self._gec_to_name
    
    def get_countries_by_region(self, region: str) -> List[Dict]:
        """
        Get all countries in a specific region.
        
        Args:
            region: Region name to filter by
            
        Returns:
            List of country dictionaries in the specified region
        """
        countries = self.load_countries()
        return [country for country in countries if country.get('region') == region]
    
    def get_regions_list(self) -> List[str]:
        """
        Get list of all available regions.
        
        Returns:
            List of unique region names
        """
        regions = set()
        for region in self._gec_to_region.values():
            if region:
                regions.add(region)
        return sorted(list(regions))
    
    def get_country_info(self, gec_code: str) -> Optional[Dict]:
        """
        Get complete country information for a given GEC code.
        
        Args:
            gec_code: GEC country code
            
        Returns:
            Dictionary with country info or None if not found
        """
        code = gec_code.lower()
        
        if code not in self._gec_to_name:
            return None
        
        return {
            'code': code,
            'name': self._gec_to_name[code],
            'region': self._gec_to_region.get(code, '')
        }
    
    def reload_config(self) -> None:
        """Reload the configuration from files."""
        logger.info("Reloading configuration...")
        self._countries_data = None
        self._gec_to_name.clear()
        self._gec_to_region.clear()
        self._load_countries_config()


# Global configuration loader instance
_config_loader: Optional[ConfigLoader] = None


def get_config_loader() -> ConfigLoader:
    """
    Get the global configuration loader instance.
    
    Returns:
        ConfigLoader instance
    """
    global _config_loader
    
    if _config_loader is None:
        _config_loader = ConfigLoader()
    
    return _config_loader


def load_countries() -> List[Dict]:
    """Load countries from configuration using global loader."""
    return get_config_loader().load_countries()


def get_country_name(gec_code: str) -> Optional[str]:
    """Get country name using global loader."""
    return get_config_loader().get_country_name(gec_code)


def get_country_region(gec_code: str) -> Optional[str]:
    """Get country region using global loader."""
    return get_config_loader().get_country_region(gec_code)


def validate_country_code(gec_code: str) -> bool:
    """Validate country code using global loader."""
    return get_config_loader().validate_country_code(gec_code)


def get_all_countries() -> Dict[str, str]:
    """Get all country mappings using global loader."""
    return get_config_loader().get_all_countries()


def get_all_regions() -> Dict[str, str]:
    """Get all region mappings using global loader."""
    return get_config_loader().get_all_regions()
