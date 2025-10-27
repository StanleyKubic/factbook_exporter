# Usage Guide

This guide provides detailed instructions for using the CIA Factbook Exporter.

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

## Command Line Interface

The application provides both interactive and command-line modes.

### Command Line Options

```bash
python main.py [OPTIONS]
```

**Options:**
- `--countries, -c`: Comma-separated country codes (e.g., fr,gm,uk)
- `--output, -o`: Output Excel filename (default: countries_data.xlsx)
- `--interactive, -i`: Interactive mode with prompts
- `--verbose, -v`: Verbose output
- `--profile, -p`: Field selection profile
- `--list-profiles`: List available field profiles and exit
- `--help`: Show help message

### Usage Examples

#### Basic Country Export
```bash
python main.py --countries fr,us,uk
```

#### Custom Output File
```bash
python main.py --countries fr,de,pl --output european_countries.xlsx
```

#### Using Field Profiles
```bash
# Economic focus
python main.py --countries fr,de,pl --profile economy

# Geographic focus
python main.py --countries br,ar,cl --profile geography

# Minimal data
python main.py --countries jp,kr,cn --profile minimal
```

#### Verbose Output
```bash
python main.py --countries fr,us,uk --verbose
```

#### Interactive Mode
```bash
python main.py --interactive
```

### Interactive Mode

Interactive mode provides a user-friendly interface with:

1. **Country Selection**: Browse countries by region
2. **Profile Selection**: Choose from available field profiles
3. **Output Customization**: Set custom filename
4. **Real-time Feedback**: See progress and results

Example Interactive Session:
```
============================================================
CIA Factbook JSON to Excel Exporter v1.3
============================================================

Available countries by region:

Europe:
  • fr (France)
  • gm (Germany)
  • uk (United Kingdom)
  • it (Italy)
  • sp (Spain)

Asia:
  • ch (China)
  • ja (Japan)
  • in (India)
  • ks (South Korea)

Enter country codes (comma-separated): fr,gm,uk
Output filename [countries_data.xlsx]: european_data.xlsx
```

## Field Profiles

Field profiles allow you to select different sets of data fields based on your needs.

### Available Profiles

#### minimal
Essential country information (5 fields):
- Background
- Location
- Area (comparative)
- Population
- Capital

#### standard
Balanced export for general use (15 fields):
- Background, Location, Geographic coordinates
- Area, Climate, Terrain, Natural resources
- Population, Nationality
- GDP, GDP growth rate
- Government type, Capital
- Internet users, Military expenditures

#### geography
Geographic intelligence focus (10 fields):
- Location, Geographic coordinates
- Area, Climate, Terrain
- Elevation (highest/lowest points)
- Natural resources, Land use
- Climate details

#### economy
Economic analysis focus (12 fields):
- Background, Location, Population
- GDP, GDP growth rate, GDP per capita
- Inflation rate, Unemployment rate
- Budget (revenues/expenditures)
- Public debt, Exports

#### comprehensive
All available fields for complete analysis (20 fields):
Combines essential fields from all categories for thorough analysis.

### Listing Available Profiles
```bash
python main.py --list-profiles
```

Output:
```
Available field profiles:
  minimal: Essential country information only (5 fields)
  standard: Balanced export for general OSINT (15 fields)
  geography: Geographic intelligence focus (10 fields)
  economy: Economic analysis focus (12 fields)
  comprehensive: All available fields for complete analysis (20 fields)
```

## Country Codes

The application uses GEC (formerly FIPS) country codes, not ISO codes.

### Common Country Codes

#### Europe
- `fr` - France
- `gm` - Germany
- `uk` - United Kingdom
- `it` - Italy
- `sp` - Spain
- `au` - Austria

#### North America
- `us` - United States
- `ca` - Canada
- `mx` - Mexico

#### Asia
- `ch` - China
- `ja` - Japan
- `in` - India
- `ks` - South Korea

#### Other Regions
- `as` - Australia
- `br` - Brazil
- `ar` - Argentina
- `sf` - South Africa
- `eg` - Egypt
- `ni` - Nigeria
- `rs` - Russia

### Viewing All Available Countries

Use interactive mode to browse all available countries organized by region:
```bash
python main.py --interactive
```

## Output

### Excel File Location
- **Directory**: `output/` (created automatically)
- **Filename**: Customizable via `--output` option
- **Sheet Name**: `Countries Data`

### Excel Formatting
- Auto-sized columns for readability
- Bold, colored headers
- Frozen header row for easy scrolling
- Clean, professional layout

### Sample Output Structure

| Country Code | Country Name | Background | Location | Area - Comparative | Climate | Population | GDP |
|--------------|--------------|------------|-----------|------------------|----------|------------|-----|
| fr | France | France today is... | Metropolitan France... | slightly more than... | generally cool winters... | 68,084,217 | $2.96 trillion |
| gm | Germany | Europe's largest economy... | Central Europe... | slightly smaller than Montana... | temperate and marine... | 83,294,633 | $4.26 trillion |

## Error Handling

The application handles errors gracefully:

### Common Issues and Solutions

#### Invalid Country Codes
**Error**: `Invalid country codes: xx,yy`
**Solution**: Verify you're using GEC codes, not ISO codes. Check the interactive mode for valid codes.

#### Network Issues
**Error**: `Failed to fetch country data`
**Solution**: Check internet connection and GitHub accessibility.

#### Missing Fields
**Warning**: Field unavailable for certain countries
**Solution**: This is normal - not all fields are available for all countries.

#### File Permissions
**Error**: `Permission denied` when creating output
**Solution**: Ensure write permissions in the project directory.

### Verbose Mode for Debugging

Use `--verbose` flag to see detailed processing information:
```bash
python main.py --countries fr,us --verbose
```

This will show:
- Country validation details
- Field loading information
- Processing progress
- Export statistics

## Performance Tips

### Large Country Lists
When processing many countries:
- The application includes delays between requests to be respectful to GitHub
- Consider batching large exports into smaller groups
- Use verbose mode to monitor progress

### Network Considerations
- Each country requires a separate API call to GitHub
- Processing time depends on network speed and GitHub API responsiveness
- Failed countries are skipped and don't affect successful exports

## Best Practices

1. **Start Interactive**: Use interactive mode first to explore available countries and profiles
2. **Test Small**: Test with 2-3 countries before large batch exports
3. **Use Profiles**: Select appropriate field profiles to avoid unnecessary data
4. **Check Output**: Verify Excel output contains expected data before processing large lists
5. **Monitor Progress**: Use verbose mode for long-running operations
