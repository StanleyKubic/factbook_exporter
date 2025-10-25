"""
Configuration module for CIA Factbook JSON to Excel Exporter.

Contains all settings, country mappings, and field definitions.
"""

# GEC code to region mapping
GEC_TO_REGION = {
    "fr": "europe",
    "gm": "europe", 
    "uk": "europe",
    "sp": "europe",
    "it": "europe",
    "au": "europe",
    "us": "north-america",
    "ca": "north-america",
    "mx": "north-america",
    "br": "south-america",
    "ar": "south-america",
    "ch": "east-n-southeast-asia",
    "ja": "east-n-southeast-asia",
    "in": "south-asia",
    "ks": "east-n-southeast-asia",
    "as": "australia-oceania",
    "sf": "africa",
    "eg": "africa",
    "ni": "africa",
    "rs": "central-asia"
}

# GEC code to country name mapping
GEC_TO_NAME = {
    "fr": "France",
    "gm": "Germany",
    "uk": "United Kingdom", 
    "sp": "Spain",
    "it": "Italy",
    "au": "Austria",
    "us": "United States",
    "ca": "Canada",
    "mx": "Mexico",
    "br": "Brazil",
    "ar": "Argentina",
    "ch": "China",
    "ja": "Japan",
    "in": "India",
    "ks": "South Korea",
    "as": "Australia",
    "sf": "South Africa",
    "eg": "Egypt",
    "ni": "Nigeria",
    "rs": "Russia"
}

# Section definitions: JSON path to column name mapping
SECTION_DEFINITIONS = {
    "Introduction.Background": "Background",
    "Geography.Location": "Location",
    "Geography.Area": "Total Area",
    "Geography.Population": "Population",
    "People and Society.Population": "Population Count",
    "Economy.Real GDP (purchasing power parity)": "GDP PPP",
    "Economy.Real GDP growth rate": "GDP Growth"
}

# URL configuration
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
