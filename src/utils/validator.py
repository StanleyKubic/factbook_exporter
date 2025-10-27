from typing import List, Tuple
from src.config.config_loader import load_countries, get_country_name as get_country_name_from_config

def validate_country_codes(codes: List[str]) -> Tuple[List[str], List[str]]:
    """
    Validate country codes against available countries in config.
    
    Args:
        codes: List of country codes to validate
        
    Returns:
        Tuple of (valid_codes, invalid_codes)
    """
    countries = load_countries()
    available_codes = {c['code'].lower() for c in countries}
    
    valid = []
    invalid = []
    
    for code in codes:
        code_lower = code.strip().lower()
        if code_lower in available_codes:
            valid.append(code_lower)
        else:
            invalid.append(code)
    
    return valid, invalid

def get_country_name(code: str) -> str:
    """
    Get country name for a given code.
    
    Args:
        code: Country code (e.g., 'fr')
        
    Returns:
        Country name or empty string if not found
    """
    # Use the efficient config_loader implementation
    name = get_country_name_from_config(code)
    return name if name is not None else ""
