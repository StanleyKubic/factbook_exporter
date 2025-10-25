"""
Text cleaner module for CIA Factbook JSON to Excel Exporter.

Handles HTML tag removal and text cleaning from extracted data.
"""

from bs4 import BeautifulSoup
from typing import Optional


def clean_text_html(text: Optional[str]) -> str:
    """
    Remove HTML tags from text and return clean plain text.
    
    Args:
        text: Input text that may contain HTML markup
        
    Returns:
        Clean text with HTML removed, or empty string if input is None
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Parse HTML and extract clean text
    soup = BeautifulSoup(text, 'html.parser')
    clean_text = soup.get_text(separator=' ', strip=True)
    
    return clean_text


def clean_value(value) -> str:
    """
    Clean any value (string, dict, list, etc.) and return clean text.
    
    Args:
        value: Any value that needs cleaning
        
    Returns:
        Clean text string
    """
    if value is None:
        return ""
    
    if isinstance(value, str):
        return clean_text_html(value)
    elif isinstance(value, dict):
        # Handle dict objects that might have 'text' field
        if 'text' in value:
            return clean_text_html(value['text'])
        else:
            # Convert dict to string and clean
            return clean_text_html(str(value))
    elif isinstance(value, list):
        # Handle lists by joining and cleaning
        if value:
            clean_items = [clean_text_html(str(item)) for item in value]
            return ', '.join(clean_items)
        return ""
    else:
        # Convert other types to string and clean
        return clean_text_html(str(value))
