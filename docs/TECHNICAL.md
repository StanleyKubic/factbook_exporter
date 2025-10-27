# Technical Documentation

This document provides technical details about the CIA Factbook Exporter architecture, dependencies, and data sources.

## Architecture Overview

The application follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Interface│    │  Business Logic  │    │   Data Layer    │
│                 │    │                  │    │                 │
│ • CLI Options   │◄──►│ • Main Orchestr. │◄──►│ • Data Fetcher  │
│ • Interactive   │    │ • Config Loader  │    │ • Data Parser   │
│ • Validation    │    │ • Field Profiles │    │ • Excel Exporter│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Utilities       │
                       │                  │
                       │ • HTML Cleaner   │
                       │ • Validator      │
                       │ • UI Helpers     │
                       └──────────────────┘
```

## Core Components

### Main Application (`main.py`)
- **Framework**: Click-based CLI interface
- **Purpose**: Application orchestration and user interaction
- **Key Features**:
  - Command-line argument parsing
  - Interactive mode support
  - Progress tracking and user feedback
  - Error handling and logging

### Data Layer

#### Data Fetcher (`fetcher.py`)
- **Purpose**: Retrieve country data from GitHub API
- **Data Source**: CIA Factbook JSON repository
- **Features**:
  - HTTP request handling with retries
  - Rate limiting and error recovery
  - JSON data validation
  - Network timeout management

#### Data Parser (`parser.py`)
- **Purpose**: Extract relevant fields from JSON data
- **Features**:
  - Dynamic field extraction based on profiles
  - JSON path navigation
  - Data type conversion and validation
  - Missing data handling

#### Excel Exporter (`exporter.py`)
- **Purpose**: Generate formatted Excel files
- **Features**:
  - Auto-sized columns
  - Professional formatting
  - Multiple sheet support capability
  - File size optimization

### Configuration System

#### Config Loader (`config_loader.py`)
- **Purpose**: Load and validate configuration files
- **Features**:
  - YAML file parsing
  - Configuration validation
  - Fallback support
  - Profile management

#### Field Profiles (`config/field_profiles.yaml`)
- **Purpose**: Define field selection sets
- **Structure**: Hierarchical profile definitions
- **Features**:
  - Reusable field groups
  - Metadata support
  - Default profile specification

### Utilities

#### HTML Cleaner (`cleaner.py`)
- **Purpose**: Remove HTML markup from text data
- **Technology**: BeautifulSoup4 with lxml parser
- **Features**:
  - Safe HTML tag removal
  - Entity decoding
  - Text normalization
  - Nested structure handling

#### Validator (`validator.py`)
- **Purpose**: Validate user input and data
- **Features**:
  - Country code validation
  - Field path verification
  - Configuration syntax checking

#### UI Helpers (`ui_helpers.py`)
- **Purpose**: Provide consistent user interface elements
- **Technology**: Rich library for terminal output
- **Features**:
  - Progress bars
  - Colored output
  - Formatted tables
  - Status indicators

## Version History

### v1.0 - Initial Release
**Core Functionality**:
- Hardcoded country mappings (20 countries)
- Basic data fetching and parsing
- Simple Excel export
- Command-line interface

**Architecture**:
- Monolithic configuration in `config.py`
- Fixed field definitions
- Basic error handling

### v1.1 - Data Quality Improvements
**Enhancements**:
- HTML cleaning module (`cleaner.py`)
- BeautifulSoup4 integration
- lxml parser for performance
- Improved text processing

**Benefits**:
- Clean, readable text output
- Removal of HTML artifacts
- Better data quality

### v1.2 - Configuration System
**Major Changes**:
- External YAML configuration (`config/countries.yaml`)
- Dynamic configuration loading (`config_loader.py`)
- Expanded country support (250+ countries)
- Region-based organization

**New Features**:
- Automated country database generation
- Configuration management scripts
- Coverage analysis tools
- Fallback configuration support

### v1.3 - Field Configuration System
**Major Changes**:
- External field configuration (`config/fields.yaml`)
- Field profiles system (`config/field_profiles.yaml`)
- Dynamic field extraction
- Profile-based field selection

**New Features**:
- 5 predefined field profiles
- Configurable field selection
- Field coverage analysis
- No-code field management

## Dependencies

### Core Dependencies
```python
requests>=2.28.0      # HTTP client for data fetching
pandas>=1.5.0         # Data manipulation and Excel export
openpyxl>=3.0.10      # Advanced Excel formatting
click>=8.0.0          # Command-line interface framework
pyyaml>=6.0           # YAML configuration parsing
```

### Data Processing
```python
beautifulsoup4>=4.11.0  # HTML parsing and cleaning
lxml>=4.9.0              # Fast XML/HTML parser backend
```

### User Interface
```python
rich>=13.0.0            # Terminal formatting and progress bars
```

### Development Dependencies
```python
pytest>=7.0.0           # Testing framework
black>=22.0.0            # Code formatting
flake8>=5.0.0            # Linting
```

## Data Source

### CIA World Factbook JSON Repository
- **URL**: https://github.com/factbook/factbook.json
- **Format**: JSON files organized by geographic regions
- **Update Frequency**: Weekly automated updates
- **License**: Public domain (U.S. government work)

### Data Structure

#### Regional Organization
```
factbook.json/
├── africa/
│   ├── ai.json          # Angola
│   ├── cg.json          # Congo
│   └── ...
├── asia/
│   ├── ch.json          # China
│   ├── ja.json          # Japan
│   └── ...
├── europe/
│   ├── fr.json          # France
│   ├── gm.json          # Germany
│   └── ...
└── ...
```

#### Country Data Format
```json
{
  "Government": {
    "Capital": {
      "name": {
        "text": "Paris",
        "html": "<strong>Paris</strong>"
      }
    },
    "Government type": {
      "text": "semi-presidential republic",
      "html": "semi-presidential <strong>republic</strong>"
    }
  },
  "Geography": {
    "Location": {
      "text": "Metropolitan France...",
      "html": "Metropolitan <strong>France</strong>..."
    }
  }
}
```

#### Field Path Convention
- **Format**: `Category.Subcategory[.Subcategory].property`
- **Example**: `Geography.Location.text`
- **Properties**:
  - `text`: Clean text content
  - `html`: Original HTML content

## Performance Characteristics

### Data Fetching
- **Rate Limiting**: 0.5 second delay between requests
- **Timeout**: 30 seconds per request
- **Retry Logic**: Up to 3 retries with exponential backoff
- **Concurrent Processing**: Sequential processing to respect API limits

### Memory Usage
- **Per Country**: ~50-100 KB JSON data
- **Processing**: In-memory parsing, no disk I/O during processing
- **Excel Generation**: Streaming writes to minimize memory footprint

### Typical Performance Metrics
- **Single Country**: 2-5 seconds (including network latency)
- **10 Countries**: 30-60 seconds
- **50 Countries**: 3-5 minutes
- **250 Countries**: 15-25 minutes

## Error Handling Strategy

### Network Errors
- **Timeout Handling**: Automatic retry with increased timeout
- **Connection Failures**: Graceful degradation with error logging
- **Rate Limiting**: Respectful API usage with delays

### Data Errors
- **Invalid JSON**: Skip affected countries, continue processing
- **Missing Fields**: Use empty values, log warnings
- **Malformed Data**: HTML cleaning for text normalization

### Configuration Errors
- **Invalid YAML**: Clear error messages with line numbers
- **Missing Profiles**: Fallback to default profile
- **Invalid Country Codes**: Validation with helpful suggestions

## Logging Configuration

### Log Levels
- **INFO**: Progress updates and success messages
- **WARNING**: Non-critical issues and skipped items
- **ERROR**: Critical failures and exceptions
- **DEBUG**: Detailed debugging information (when enabled)

### Log Format
```
YYYY-MM-DD HH:MM:SS - module_name - LEVEL - message
```

### Log Destinations
- **Console**: User-facing progress and error messages
- **File**: Detailed application logs (optional)

## Security Considerations

### Data Privacy
- **No Personal Data**: Only processes public government data
- **Local Processing**: All data processing occurs locally
- **No Data Transmission**: Only fetches from public GitHub repository

### Input Validation
- **Country Code Validation**: Prevents path traversal
- **File Name Validation**: Prevents directory traversal
- **YAML Parsing**: Safe loading to prevent code execution

### Network Security
- **HTTPS Only**: All network requests use HTTPS
- **Certificate Validation**: Proper SSL certificate verification
- **Timeout Protection**: Prevents hanging connections

## Extensibility

### Adding New Data Sources
The modular architecture allows adding new data sources:
1. Implement new fetcher class
2. Add parser for new data format
3. Update configuration schema
4. Maintain existing interface

### Custom Export Formats
The exporter module supports multiple formats:
1. Excel (current implementation)
2. CSV (planned)
3. JSON (planned)
4. Database integration (planned)

### Field Transformations
The parser supports custom field transformations:
1. Data type conversion
2. Unit standardization
3. Currency conversion
4. Date format normalization

## Code Quality Standards

### Style Guidelines
- **Formatter**: Black for consistent formatting
- **Linter**: Flake8 for code quality
- **Type Hints**: Full type annotation coverage
- **Documentation**: Docstrings for all public functions

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Mock Services**: Network request mocking
- **Data Validation**: Output format verification

### Performance Monitoring
- **Timing Metrics**: Request duration tracking
- **Memory Usage**: Memory consumption monitoring
- **Success Rates**: Data fetch success tracking
- **Error Analysis**: Error pattern identification
