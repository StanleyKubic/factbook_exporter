# CIA Factbook JSON to Excel Exporter v1.3

A Python application that extracts country data from CIA World Factbook JSON repository and exports selected fields to Excel format.

## Version History

### v1.0 - Initial Release
- **All hardcoded configurations**: Country mappings, regions, and field definitions were hardcoded in `config.py`
- **Basic functionality**: Data fetching, parsing, and Excel export
- **Limited country support**: 20 pre-selected countries across 7 regions

### v1.1 - Data Quality Improvements
- **HTML cleaning implementation**: Added `cleaner.py` module for removing HTML tags and entities
- **Enhanced text processing**: Automatic cleanup of HTML markup from extracted text data
- **Improved data quality**: Clean, readable text output with proper spacing

### v1.2 - Configuration File Support
- **External country configuration**: Migrated country data to `config/countries.yaml`
- **Config loader module**: Added `config_loader.py` for dynamic configuration loading
- **Expanded country database**: Support for 250+ countries and territories
- **Region-based organization**: Countries organized by geographic regions
- **Configuration generation script**: `scripts/generate_countries.py` for updating country data

### v1.3 - Field Configuration System
- **Dynamic field configuration**: Migrated field definitions to `config/fields.yaml`
- **Configurable field selection**: User can customize exported fields via YAML configuration
- **Enhanced field management**: 19 high-coverage fields pre-configured
- **Improved categorization**: Fields organized by categories (Geography, Government, Introduction, Environment)
- **Flexible architecture**: No code changes needed for field modifications

## Features

- **Data Source**: CIA World Factbook JSON repository (https://github.com/factbook/factbook.json)
- **Interactive Interface**: Command-line interface with user input
- **Comprehensive Country Support**: 250+ countries and territories across all geographic regions
- **Dynamic Configuration**: External YAML configuration for countries and fields
- **HTML Cleaning**: Automatic removal of HTML tags and entities from extracted text (v1.1+)
- **Error Handling**: Graceful handling of missing data and network issues
- **Excel Export**: Formatted Excel files with auto-sized columns and styling
- **Comprehensive Logging**: Detailed progress reporting and error tracking
- **Configuration Management**: Flexible country and field data loading with config generation tools (v1.2+)
- **Region-based Organization**: Countries organized by geographic regions for easy selection
- **Field Customization**: Configurable field selection and categorization (v1.3+)
- **Extensible Architecture**: Modular design for easy maintenance and enhancement

## Supported Countries

The application supports **250+ countries and territories** across all geographic regions, loaded dynamically from `config/countries.yaml`. The configuration includes:

### Major Regions
- **Africa** (58+ countries)
- **Asia** (50+ countries) 
- **Europe** (50+ countries)
- **Middle East** (20+ countries)
- **North America** (40+ countries)
- **South America** (15+ countries)
- **Australia-Oceania** (25+ countries)
- **Central Asia** (5+ countries)
- **Antarctica & Oceans** (5+ territories)

### Popular Examples
Here are some commonly used country codes:

#### Europe
- `fr` - France, `gm` - Germany, `uk` - United Kingdom
- `sp` - Spain, `it` - Italy, `au` - Austria

#### North America  
- `us` - United States, `ca` - Canada, `mx` - Mexico

#### Asia
- `ch` - China, `ja` - Japan, `in` - India, `ks` - South Korea

#### Other Regions
- `as` - Australia, `br` - Brazil, `ar` - Argentina
- `sf` - South Africa, `eg` - Egypt, `ni` - Nigeria
- `rs` - Russia

### Configuration Management
The country list is maintained in `config/countries.yaml` and can be updated using:
```bash
python3 scripts/generate_countries.py
```

This script fetches the latest country data from the CIA Factbook repository and updates the configuration file automatically.

## Extracted Fields

The application extracts **configurable fields** for each country, loaded from `config/fields.yaml`.

**Benefits of field configuration:**
- **Customizable**: Easy to add/remove fields by editing YAML
- **Categorized**: Automatic grouping by category
- **Coverage-based**: Pre-filtered by data availability
- **Maintainable**: No code changes required

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup

1. Clone or download the project:
```bash
cd factbook_exporter
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Virtual Environment Usage

#### Option 1: Manual Activation
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

#### Option 2: Using the Activation Script (Linux/macOS)
```bash
./activate.sh
python main.py
```

To deactivate the virtual environment when done:
```bash
deactivate
```

## Usage

### Running the Application

```bash
# Make sure virtual environment is activated first
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the application
python main.py
```

### Example Session

```
============================================================
CIA Factbook JSON to Excel Exporter v1.3
============================================================

This tool extracts country data from the CIA World Factbook
and exports selected fields to an Excel file.

Supported country codes (GEC format):

Africa:
  • eg (Egypt)
  • ni (Nigeria)
  • sf (South Africa)

Europe:
  • fr (France)
  • gm (Germany)
  • uk (United Kingdom)
  ...

============================================================

Enter country codes (comma-separated, e.g., fr,gm,au): fr,us,ch,as

Processing 4 countries...
----------------------------------------
Step 1: Fetching data from CIA Factbook...
Successfully fetched data for 4 countries

Step 2: Parsing extracted fields...
Successfully parsed data for 4 countries

Field availability summary:
  • Country Code: 4/4 countries
  • Country Name: 4/4 countries
  • Background: 4/4 countries
  • Location: 4/4 countries
  • Area - Comparative: 4/4 countries
  • Climate: 4/4 countries
  • ...

Step 3: Exporting to Excel...
✓ Success! Excel file created: /path/to/output/countries_data.xlsx

Export Summary:
  • Countries processed: 4
  • Fields extracted: 19
  • Output file: /path/to/output/countries_data.xlsx
  • File size: 15,432 bytes

============================================================
Export completed successfully!
============================================================
```

## Output

### Excel File Location
- **Directory**: `output/` (created automatically)
- **Filename**: `countries_data.xlsx`
- **Sheet Name**: `Countries Data`

### Excel Formatting
- Auto-sized columns for readability
- Bold, colored headers
- Frozen header row for easy scrolling
- Clean, professional layout

### HTML Cleaning

The application automatically removes HTML tags and entities from extracted text:

- **Removes**: `<strong>`, `<em>`, `<a href>`, `<br/>`, `<p>`, `<span>` tags
- **Cleans**: HTML entities like `&nbsp;`, `&`, `"`
- **Preserves**: Readable text content with proper spacing
- **Handles**: Complex nested HTML structures safely

**Before**: "France is a <strong>landlocked</strong> country in <em>Western Europe</em><br/>bordering..."  
**After**: "France is a landlocked country in Western Europe bordering..."

### Data Structure
| Country Code | Country Name | Background | Location | Area - Comparative | Climate | Geographic Coordinates | ... | Natural Hazards | Terrain |
|--------------|--------------|------------|-----------|------------------|----------|----------------------|-----|----------------|---------|

## Project Structure

```
factbook_exporter/
├── main.py                    # Entry point and orchestration
├── config.py                  # Core configuration settings (v1.0)
├── config_loader.py           # Dynamic configuration loading (v1.2+)
├── fetcher.py                 # Data retrieval from GitHub
├── parser.py                  # JSON data extraction with dynamic fields (v1.3+)
├── exporter.py                # Excel file generation
├── cleaner.py                 # HTML cleaning and text processing (v1.1+)
├── requirements.txt           # Python dependencies
├── config/                    # Configuration files directory (v1.2+)
│   ├── countries.yaml         # Country and region mappings
│   └── fields.yaml          # Field definitions and mappings (v1.3+)
├── scripts/                   # Utility and maintenance scripts
│   ├── generate_countries.py  # Country configuration generator
│   ├── analyze_coverage.py    # Data coverage analysis tool
│   └── analyze_coverage_simple.py # Simplified coverage analysis
├── reports/                   # Generated reports and analysis
│   ├── coverage_report.yaml   # Data coverage analysis results
│   └── coverage_simple.yaml  # Simplified coverage data for field selection
└── output/                    # Generated Excel files
```

### Key Components by Version

#### v1.0 - Core Components
- `main.py` - Application orchestration and user interface
- `config.py` - Hardcoded country mappings and settings
- `fetcher.py` - GitHub API data retrieval
- `parser.py` - JSON parsing and field extraction
- `exporter.py` - Excel file generation and formatting

#### v1.1 - Data Quality Enhancement
- `cleaner.py` - HTML tag removal and text cleaning using BeautifulSoup

#### v1.2 - Configuration System
- `config_loader.py` - Dynamic YAML configuration loading
- `config/countries.yaml` - External country database (250+ countries)
- `scripts/generate_countries.py` - Automated configuration updates
- `scripts/analyze_coverage.py` - Data analysis and reporting tools

#### v1.3 - Field Configuration System
- `config/fields.yaml` - External field definitions (19 high-coverage fields)
- Enhanced `config_loader.py` - Field loading and categorization support
- Updated `parser.py` - Dynamic field extraction from configuration
- `scripts/analyze_coverage_simple.py` - Coverage data for field selection

## Error Handling

The application handles errors gracefully:

- **Invalid Country Codes**: Skips invalid codes with warnings
- **Network Issues**: Logs errors and continues with other countries
- **Missing Fields**: Uses empty values for unavailable data
- **File Permissions**: Creates directories and handles write errors
- **Configuration Errors**: Validates field and country configurations

## Configuration System

### Country Configuration (v1.2+)

The application uses a flexible YAML-based configuration system for country management:

#### Configuration File Structure
```yaml
countries:
  - code: fr
    name: France
    region: europe
  - code: us
    name: United States
    region: north-america
  # ... more countries
```

#### Configuration Loading
- **Primary Source**: `config/countries.yaml` (250+ countries)
- **Fallback**: `config.py` hardcoded mappings (v1.0 compatibility)
- **Loader Module**: `config_loader.py` provides unified access

#### Configuration Management
```bash
# Update country database from CIA Factbook
python3 scripts/generate_countries.py

# Analyze data coverage across countries
python3 scripts/analyze_coverage.py
```

### Field Configuration (v1.3+)

Field definitions are now maintained externally in `config/fields.yaml`:

#### Configuration File Structure
```yaml
fields:
  - json_path: "Geography.Location.text"
    display_name: "Location"
    category: "Geography"
    coverage_pct: 100.0
  - json_path: "Introduction.Background.text"
    display_name: "Background"
    category: "Introduction"
    coverage_pct: 100.0
  # ... more fields
```

#### Field Loading
- **Primary Source**: `config/fields.yaml` (19 pre-selected high-coverage fields)
- **Loader Module**: `config_loader.py` provides field access methods
- **Parser Integration**: `parser.py` uses dynamic field mappings

#### Field Management
```bash
# Analyze coverage to find best fields
python3 scripts/analyze_coverage_simple.py

# Edit fields configuration
vim config/fields.yaml
```

#### Field Benefits
- **Configurable**: Easy to modify without code changes
- **Categorized**: Automatic grouping by section (Geography, Government, etc.)
- **Coverage-based**: Pre-filtered for high data availability
- **Extensible**: Unlimited field support

## Technical Details

### Dependencies
- `requests` - HTTP requests for data fetching
- `pandas` - Data manipulation and Excel export
- `openpyxl` - Advanced Excel formatting
- `beautifulsoup4` - HTML parsing and text cleaning (v1.1+)
- `lxml` - Fast HTML parser backend for BeautifulSoup (v1.1+)
- `pyyaml` - YAML configuration file parsing (v1.2+)

### Data Source
- **Repository**: https://github.com/factbook/factbook.json
- **Format**: JSON files organized by geographic regions
- **Update Frequency**: Weekly (automated updates)

### GEC Codes
The application uses GEC (formerly FIPS) country codes, not ISO codes:
- `fr` = France (not `at`)
- `gm` = Germany (not `de`)
- `au` = Austria (not `at`)

## Logging

The application provides comprehensive logging:
- **INFO**: Progress updates and success messages
- **WARNING**: Non-critical issues and skipped items
- **ERROR**: Critical failures and exceptions

## Development Roadmap

### v1.4 - Enhanced Features (Future)
- **Batch processing**: Process country lists from external files
- **Custom output formats**: Support for CSV, JSON, and other formats
- **Advanced filtering**: Region-based and criteria-based country selection
- **Performance optimization**: Parallel processing for large datasets
- **Field validation**: Data quality checks and validation rules

### v2.0 - Major Enhancements (Future)
- **Graphical user interface**: Web-based UI using Streamlit
- **API endpoints**: RESTful API for programmatic access
- **Database integration**: Local caching and history tracking
- **Advanced reporting**: Statistical analysis and visualization

### Completed Features

✅ **v1.0 - Core Functionality**
- Basic data fetching, parsing, and Excel export
- 20 pre-selected countries with hardcoded configuration

✅ **v1.1 - Data Quality**
- HTML cleaning and text processing using BeautifulSoup
- Improved data extraction and formatting

✅ **v1.2 - Configuration System**
- External YAML configuration for 250+ countries
- Dynamic configuration loading with fallback support
- Automated configuration generation and analysis tools

✅ **v1.3 - Field Configuration**
- External YAML configuration for field definitions
- 19 high-coverage fields pre-configured
- Dynamic field extraction and categorization
- Flexible field management without code changes

## Troubleshooting

### Common Issues

1. **"Country code not found"**
   - Verify you're using GEC codes, not ISO codes
   - Check supported countries list

2. **"Network error"**
   - Check internet connection
   - Verify GitHub accessibility

3. **"Permission denied"**
   - Ensure write permissions in project directory
   - Check if output directory is accessible

4. **"Field not found"**
   - Verify field configuration in `config/fields.yaml`
   - Check JSON paths are correct
   - Run coverage analysis to validate field availability

### Getting Help

For issues or questions:
1. Check the logs for detailed error messages
2. Verify country codes are valid GEC format
3. Ensure all dependencies are installed correctly
4. Validate configuration files are properly formatted

## License

This project is provided as-is for educational and research purposes.

## Data Source Attribution

Country data sourced from the CIA World Factbook, maintained by the U.S. Central Intelligence Agency.
Repository: https://github.com/factbook/factbook.json
