# CIA Factbook JSON to Excel Exporter v1.0

A Python application that extracts country data from the CIA World Factbook JSON repository and exports selected fields to Excel format.

## Features

- **Data Source**: CIA World Factbook JSON repository (https://github.com/factbook/factbook.json)
- **Interactive Interface**: Command-line interface with user input
- **Multi-region Support**: 20 countries across 7 geographic regions
- **HTML Cleaning**: Automatic removal of HTML tags and entities from extracted text
- **Error Handling**: Graceful handling of missing data and network issues
- **Excel Export**: Formatted Excel files with auto-sized columns and styling
- **Comprehensive Logging**: Detailed progress reporting and error tracking
  +++++++ REPLACE

## Supported Countries

The application supports 20 countries across all major regions:

### Europe (6)
- `fr` - France
- `gm` - Germany  
- `uk` - United Kingdom
- `sp` - Spain
- `it` - Italy
- `au` - Austria

### North America (3)
- `us` - United States
- `ca` - Canada
- `mx` - Mexico

### South America (2)
- `br` - Brazil
- `ar` - Argentina

### Asia (4)
- `ch` - China
- `ja` - Japan
- `in` - India
- `ks` - South Korea

### Australia-Oceania (1)
- `as` - Australia

### Africa (3)
- `sf` - South Africa
- `eg` - Egypt
- `ni` - Nigeria

### Central Asia (1)
- `rs` - Russia

## Extracted Fields

The application extracts the following 7 fields for each country:

1. **Background** - Historical and political overview
2. **Location** - Geographic description and coordinates
3. **Total Area** - Country's total land area
4. **Population Count** - Current population data
5. **GDP PPP** - Gross Domestic Product (Purchasing Power Parity)
6. **GDP Growth** - Real GDP growth rate
7. **Country Code/Name** - GEC code and full country name

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup

1. Clone or download the project:
```bash
cd factbook_exporter
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

### Running the Application

```bash
python3 main.py
```

### Example Session

```
============================================================
CIA Factbook JSON to Excel Exporter v1.0
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

Step 3: Exporting to Excel...
✓ Success! Excel file created: /path/to/output/countries_data.xlsx

Export Summary:
  • Countries processed: 4
  • Fields extracted: 9
  • Output file: /path/to/output/countries_data.xlsx
  • File size: 12,655 bytes

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
| Country Code | Country Name | Background | Location | Total Area | Population Count | GDP PPP | GDP Growth |
|--------------|--------------|------------|-----------|-------------|-----------------|----------|------------|
  +++++++ REPLACE

## Project Structure

```
factbook_exporter/
├── main.py              # Entry point and orchestration
├── config.py            # Configuration and country mappings
├── fetcher.py           # Data retrieval from GitHub
├── parser.py            # JSON data extraction
├── exporter.py          # Excel file generation
├── requirements.txt     # Python dependencies
└── output/              # Generated Excel files
```

## Error Handling

The application handles errors gracefully:

- **Invalid Country Codes**: Skips invalid codes with warnings
- **Network Issues**: Logs errors and continues with other countries
- **Missing Fields**: Uses empty values for unavailable data
- **File Permissions**: Creates directories and handles write errors

## Technical Details

### Dependencies
- `requests` - HTTP requests for data fetching
- `pandas` - Data manipulation and Excel export
- `openpyxl` - Advanced Excel formatting
- `beautifulsoup4` - HTML parsing and text cleaning
- `lxml` - Fast HTML parser backend for BeautifulSoup
  +++++++ REPLACE

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

## Future Enhancements (V2)

Planned improvements for future versions:
- External configuration files (YAML/JSON)
- Graphical user interface (Streamlit/Tkinter)
- Dynamic field selection
- Extended country database
- Batch processing from file input

## Troubleshooting

### Common Issues

1. **"Country code not found"**
   - Verify you're using GEC codes, not ISO codes
   - Check the supported countries list

2. **"Network error"**
   - Check internet connection
   - Verify GitHub accessibility

3. **"Permission denied"**
   - Ensure write permissions in project directory
   - Check if output directory is accessible

### Getting Help

For issues or questions:
1. Check the logs for detailed error messages
2. Verify country codes are valid GEC format
3. Ensure all dependencies are installed correctly

## License

This project is provided as-is for educational and research purposes.

## Data Source Attribution

Country data sourced from the CIA World Factbook, maintained by the U.S. Central Intelligence Agency.
Repository: https://github.com/factbook/factbook.json
