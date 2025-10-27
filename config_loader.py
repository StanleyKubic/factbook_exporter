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

# Application-wide configuration constants
BASE_URL = "https://github.com/factbook/factbook.json/raw/master"
URL_TEMPLATE = f"{BASE_URL}/{{region}}/{{code}}.json"

# Output settings
OUTPUT_DIR = "output"
OUTPUT_FILENAME = "countries_data.xlsx"
SHEET_NAME = "Countries Data"

# Request settings
REQUEST_TIMEOUT = 30  # seconds
REQUEST_RETRY_DELAY = 1  # seconds

# Logging settings
LOG_LEVEL = "INFO"


class ConfigLoader:
    """Handles loading and accessing configuration data from YAML files."""
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize configuration loader.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self._countries_data: Optional[Dict] = None
        self._fields_data: Optional[Dict] = None
        self._profiles_data: Optional[Dict] = None
        self._gec_to_name: Dict[str, str] = {}
        self._gec_to_region: Dict[str, str] = {}
        self._json_path_to_display: Dict[str, str] = {}
        self._json_path_to_category: Dict[str, str] = {}
        
        # Load configuration on initialization
        self._load_countries_config()
        self._load_fields_config()
        self._load_profiles_config()
    
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
    
    def _load_fields_config(self) -> None:
        """Load fields configuration from YAML file."""
        fields_file = self.config_dir / "fields.yaml"
        
        if not fields_file.exists():
            # Fields configuration is optional, skip if not found
            logger.warning(f"Fields configuration file not found: {fields_file}")
            return
        
        try:
            with open(fields_file, 'r', encoding='utf-8') as f:
                self._fields_data = yaml.safe_load(f)
            
            if not self._fields_data or 'fields' not in self._fields_data:
                raise ValueError("Invalid fields configuration: missing 'fields' section")
            
            # Build lookup dictionaries for efficient access
            fields = self._fields_data['fields']
            
            for field in fields:
                json_path = field.get('json_path', '')
                display_name = field.get('display_name', '')
                category = field.get('category', '')
                
                if json_path and display_name:
                    self._json_path_to_display[json_path] = display_name
                    if category:
                        self._json_path_to_category[json_path] = category
            
            logger.info(f"Loaded {len(self._json_path_to_display)} fields from configuration")
            
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing fields configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading fields configuration: {e}")
    
    def _load_profiles_config(self) -> None:
        """Load field profiles configuration from YAML file."""
        profiles_file = self.config_dir / "field_profiles.yaml"
        
        if not profiles_file.exists():
            raise FileNotFoundError(f"Field profiles configuration file not found: {profiles_file}")
        
        try:
            with open(profiles_file, 'r', encoding='utf-8') as f:
                self._profiles_data = yaml.safe_load(f)
            
            if not self._profiles_data or 'profiles' not in self._profiles_data:
                raise ValueError("Invalid field profiles configuration: missing 'profiles' section")
            
            logger.info(f"Loaded {len(self._profiles_data['profiles'])} field profiles from configuration")
            
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing field profiles configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading field profiles configuration: {e}")
    
    def load_countries(self) -> List[Dict]:
        """
        Load complete countries list from configuration.
        
        Returns:
            List of country dictionaries with code, name, and region
        """
        if not self._countries_data:
            raise RuntimeError("Configuration not loaded")
        
        return self._countries_data.get('countries', [])
    
    def load_fields(self) -> List[Dict]:
        """
        Load complete fields list from configuration.
        
        Returns:
            List of field dictionaries with json_path, display_name, and category
        """
        if not self._fields_data:
            return []
        
        return self._fields_data.get('fields', [])
    
    def load_all_fields(self) -> List[Dict]:
        """
        Load complete fields list from fields_complete.yaml.
        
        Returns:
            List of field dictionaries with coverage data
        """
        fields_complete_file = self.config_dir / "fields_complete.yaml"
        
        if not fields_complete_file.exists():
            logger.warning(f"Complete fields configuration file not found: {fields_complete_file}")
            return []
        
        try:
            with open(fields_complete_file, 'r', encoding='utf-8') as f:
                fields_complete_data = yaml.safe_load(f)
            
            if not fields_complete_data or 'fields' not in fields_complete_data:
                raise ValueError("Invalid complete fields configuration: missing 'fields' section")
            
            return fields_complete_data.get('fields', [])
            
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing complete fields configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading complete fields configuration: {e}")
    
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
    
    def get_field_display_name(self, json_path: str) -> Optional[str]:
        """
        Get the display name for a given JSON path.
        
        Args:
            json_path: JSON path (e.g., "Geography.Location.text")
            
        Returns:
            Display name or None if path not found
        """
        return self._json_path_to_display.get(json_path)
    
    def get_field_category(self, json_path: str) -> Optional[str]:
        """
        Get the category for a given JSON path.
        
        Args:
            json_path: JSON path (e.g., "Geography.Location.text")
            
        Returns:
            Category name or None if path not found
        """
        return self._json_path_to_category.get(json_path)
    
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
    
    def get_all_field_mappings(self) -> Dict[str, str]:
        """
        Get all JSON path to display name mappings.
        
        Returns:
            Dictionary mapping JSON paths to display names
        """
        return self._json_path_to_display.copy()
    
    def get_fields_by_category(self, category: str) -> List[Dict]:
        """
        Get all fields in a specific category.
        
        Args:
            category: Category name to filter by
            
        Returns:
            List of field dictionaries in specified category
        """
        fields = self.load_fields()
        return [field for field in fields if field.get('category') == category]
    
    def get_field_categories_list(self) -> List[str]:
        """
        Get list of all available field categories.
        
        Returns:
            List of unique category names
        """
        categories = set()
        for category in self._json_path_to_category.values():
            if category:
                categories.add(category)
        return sorted(list(categories))
    
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
            List of country dictionaries in specified region
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
    
    def get_profile_fields(self, profile_name: str) -> List[str]:
        """
        Get list of field paths for a given profile.
        
        Args:
            profile_name: Name of the profile (e.g., 'minimal', 'standard')
            
        Returns:
            List of field path strings
            
        Raises:
            ValueError: If profile doesn't exist
        """
        if not self._profiles_data:
            raise RuntimeError("Profiles configuration not loaded")
        
        if profile_name not in self._profiles_data['profiles']:
            available = ', '.join(self._profiles_data['profiles'].keys())
            raise ValueError(f"Profile '{profile_name}' not found. Available: {available}")
        
        profile = self._profiles_data['profiles'][profile_name]
        fields = profile['fields']
        
        # Special case: 'all_universal' means load all universal fields
        if 'all_universal' in fields:
            # Load from fields_complete.yaml where coverage >= 95
            all_fields = self.load_all_fields()
            universal = [f['json_path'] for f in all_fields if f.get('coverage_pct', 0) >= 95]
            return universal
        
        return fields
    
    def get_default_profile(self) -> str:
        """Get the default profile name from config"""
        if not self._profiles_data:
            raise RuntimeError("Profiles configuration not loaded")
        
        return self._profiles_data['metadata'].get('default_profile', 'standard')
    
    def list_available_profiles(self) -> Dict[str, str]:
        """
        Get all available profiles with their descriptions.
        
        Returns:
            Dict mapping profile names to descriptions
        """
        if not self._profiles_data:
            raise RuntimeError("Profiles configuration not loaded")
        
        return {
            name: profile['description']
            for name, profile in self._profiles_data['profiles'].items()
        }
    
    def reload_config(self) -> None:
        """Reload configuration from files."""
        logger.info("Reloading configuration...")
        self._countries_data = None
        self._fields_data = None
        self._profiles_data = None
        self._gec_to_name.clear()
        self._gec_to_region.clear()
        self._json_path_to_display.clear()
        self._json_path_to_category.clear()
        self._load_countries_config()
        self._load_fields_config()
        self._load_profiles_config()


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


def load_fields() -> List[Dict]:
    """Load fields from configuration using global loader."""
    return get_config_loader().load_fields()


def load_all_fields() -> List[Dict]:
    """Load all fields from complete configuration using global loader."""
    return get_config_loader().load_all_fields()


def get_country_name(gec_code: str) -> Optional[str]:
    """Get country name using global loader."""
    return get_config_loader().get_country_name(gec_code)


def get_country_region(gec_code: str) -> Optional[str]:
    """Get country region using global loader."""
    return get_config_loader().get_country_region(gec_code)


def get_field_display_name(json_path: str) -> Optional[str]:
    """Get field display name using global loader."""
    return get_config_loader().get_field_display_name(json_path)


def get_field_category(json_path: str) -> Optional[str]:
    """Get field category using global loader."""
    return get_config_loader().get_field_category(json_path)


def get_all_field_mappings() -> Dict[str, str]:
    """Get all field mappings using global loader."""
    return get_config_loader().get_all_field_mappings()


def get_fields_by_category(category: str) -> List[Dict]:
    """Get fields by category using global loader."""
    return get_config_loader().get_fields_by_category(category)


def validate_country_code(gec_code: str) -> bool:
    """Validate country code using global loader."""
    return get_config_loader().validate_country_code(gec_code)


def get_all_countries() -> Dict[str, str]:
    """Get all country mappings using global loader."""
    return get_config_loader().get_all_countries()


def get_all_regions() -> Dict[str, str]:
    """Get all region mappings using global loader."""
    return get_config_loader().get_all_regions()


def load_profiles() -> Dict:
    """Load field profiles configuration using global loader."""
    return get_config_loader()._profiles_data


def get_profile_fields(profile_name: str) -> List[str]:
    """Get profile fields using global loader."""
    return get_config_loader().get_profile_fields(profile_name)


def get_default_profile() -> str:
    """Get default profile using global loader."""
    return get_config_loader().get_default_profile()


def list_available_profiles() -> Dict[str, str]:
    """List available profiles using global loader."""
    return get_config_loader().list_available_profiles()
