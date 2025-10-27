# Configuration Guide

This guide explains how to configure and customize the CIA Factbook Exporter.

## Configuration Overview

The application uses a flexible YAML-based configuration system with two main components:

1. **Country Configuration**: Maps country codes to names and regions
2. **Field Profiles**: Define which data fields to extract for different use cases

All configuration files are located in the `config/` directory.

## Country Configuration

### File Location: `config/countries.yaml`

This file contains the complete database of supported countries and territories.

### Structure

```yaml
countries:
  - code: fr
    name: France
    region: europe
  - code: us
    name: United States
    region: north-america
  - code: ch
    name: China
    region: asia
  # ... more countries
```

### Supported Regions

The application organizes countries into these geographic regions:

- **africa**: African continent countries
- **asia**: Asian countries including Central Asia
- **australia-oceania**: Australia, New Zealand, and Pacific islands
- **central-america**: Central American countries and Caribbean
- **central-asia**: Former Soviet republics in Central Asia
- **europe**: European continent countries
- **middle-east**: Middle Eastern countries
- **north-america**: North American countries
- **south-america**: South American countries
- **antarctica-oceans**: Antarctica and oceanic territories

### Adding New Countries

To add a new country:

1. Edit `config/countries.yaml`
2. Add a new entry to the countries list:

```yaml
- code: xx
  name: New Country Name
  region: appropriate-region
```

3. Verify the country code exists in the CIA Factbook data source

### Updating Country Database

The country configuration can be automatically updated from the CIA Factbook repository:

```bash
python3 scripts/generate_countries.py
```

This script:
- Fetches the latest country data from the CIA Factbook JSON repository
- Updates `config/countries.yaml` with new or modified entries
- Maintains region classifications
- Preserves custom entries

## Field Profiles Configuration

### File Location: `config/field_profiles.yaml`

This file defines field selection profiles for different export use cases.

### Structure

```yaml
metadata:
  default_profile: "standard"
  description: "Field selection profiles for different export use cases"

profiles:
  profile_name:
    description: "Human-readable description"
    fields:
      - Introduction.Background.text
      - Geography.Location.text
      # ... more field paths
```

### Field Path Format

Fields are specified using JSON paths that correspond to the CIA Factbook data structure:

```yaml
# Format: Category.Subcategory[.Subcategory].text
- Introduction.Background.text
- Geography.Location.text
- People and Society.Population.text
- Economy.GDP (purchasing power parity) - real.text
```

### Available Categories

The CIA Factbook data is organized into these main categories:

#### Introduction
- `Introduction.Background.text`: Country overview and history

#### Geography
- `Geography.Location.text`: Geographic location and borders
- `Geography.Geographic coordinates.text`: Latitude and longitude
- `Geography.Area - comparative.text`: Size comparison
- `Geography.Climate.text`: Climate description
- `Geography.Terrain.text`: Terrain features
- `Geography.Elevation extremes.text`: Highest and lowest points
- `Geography.Natural resources.text`: Available natural resources
- `Geography.Land use.text`: Agricultural and other land use

#### People and Society
- `People and Society.Population.text`: Population data
- `People and Society.Nationality.noun.text`: Demonym (e.g., "French")
- `People and Society.Ethnic groups.text`: Ethnic composition
- `People and Society.Languages.text`: Official languages
- `People and Society.Religions.text`: Religious demographics

#### Government
- `Government.Government type.text`: Form of government
- `Government.Capital.name.text`: Capital city name
- `Government.Administrative divisions.text`: Internal divisions

#### Economy
- `Economy.GDP (purchasing power parity) - real.text`: GDP value
- `Economy.GDP - per capita (PPP).text`: GDP per person
- `Economy.Real GDP growth rate.text`: Economic growth
- `Economy.Inflation rate.text`: Inflation data
- `Economy.Unemployment rate.text`: Employment statistics
- `Economy.Budget.revenues.text`: Government income
- `Economy.Budget.expenditures.text`: Government spending
- `Economy.Public debt.text`: National debt
- `Economy.Exports.text`: Export data
- `Economy.Imports.text`: Import data

#### Communications
- `Communications.Internet users.text`: Internet usage data
- `Communications.Telephones - mobile cellular.text`: Mobile phone usage

#### Military and Security
- `Military and Security.Military expenditures.text`: Defense spending

### Creating Custom Profiles

To create a new field profile:

1. Edit `config/field_profiles.yaml`
2. Add a new profile entry:

```yaml
profiles:
  my_custom_profile:
    description: "Custom profile for specific needs"
    fields:
      - Introduction.Background.text
      - Geography.Location.text
      - Geography.Area - comparative.text
      - People and Society.Population.text
      - Government.Capital.name.text
```

3. Use the profile with: `python main.py --profile my_custom_profile`

### Modifying Existing Profiles

You can modify existing profiles by changing their field lists. For example, to add internet usage to the minimal profile:

```yaml
minimal:
  description: "Essential country information only (6 fields)"
  fields:
    - Introduction.Background.text
    - Geography.Location.text
    - Geography.Area - comparative.text
    - People and Society.Population.text
    - Government.Capital.name.text
    - Communications.Internet users.text  # Added field
```

## Field Discovery and Analysis

### Coverage Analysis

To find which fields have the best data coverage across countries:

```bash
python3 scripts/analyze_coverage_simple.py
```

This script:
- Analyzes all countries in the database
- Reports data availability percentages for each field
- Helps identify high-quality fields for new profiles

The output is saved to `reports/coverage_simple.yaml`:

```yaml
fields:
  Introduction.Background.text:
    coverage_pct: 98.5
    available_countries: 247
  Geography.Location.text:
    coverage_pct: 100.0
    available_countries: 250
```

### Complete Field List

For a comprehensive list of all available fields:

```bash
python3 scripts/analyze_coverage.py
```

This generates `reports/coverage_report.yaml` with detailed coverage information for all fields.

## Configuration Validation

### Field Validation

The application validates field configurations when loading:

1. **Path Validation**: Checks if field paths follow correct format
2. **Profile Validation**: Ensures all fields in profiles exist
3. **Default Profile**: Verifies the default profile is defined

### Country Validation

Country configuration is validated during runtime:

1. **Code Uniqueness**: Ensures no duplicate country codes
2. **Region Validation**: Checks if regions are recognized
3. **Data Availability**: Verifies countries exist in the data source

## Advanced Configuration

### Custom Field Mappings

For advanced users, you can create custom field mappings by editing the field configuration files directly:

```yaml
# Custom field with display name
- json_path: "Geography.Area - comparative.text"
  display_name: "Area Size"
  category: "Geography"
  coverage_pct: 95.0
```

### Profile Inheritance

While the current system doesn't support profile inheritance, you can simulate it by creating base profiles and referencing them:

```yaml
profiles:
  base_essential:
    description: "Base essential fields"
    fields:
      - Introduction.Background.text
      - Geography.Location.text
      - People and Society.Population.text

  extended_essential:
    description: "Essential plus economic data"
    fields:
      - Introduction.Background.text
      - Geography.Location.text
      - People and Society.Population.text
      - Economy.GDP (purchasing power parity) - real.text
```

## Configuration Best Practices

### Field Selection

1. **Start Small**: Begin with essential fields and add as needed
2. **Check Coverage**: Use coverage analysis to select reliable fields
3. **Consider Use Case**: Choose fields relevant to your analysis needs
4. **Test Profiles**: Validate profiles with sample countries before bulk use

### Profile Organization

1. **Descriptive Names**: Use clear, descriptive profile names
2. **Field Count**: Keep profiles focused (5-20 fields is typical)
3. **Documentation**: Provide clear descriptions for each profile
4. **Logical Grouping**: Group related fields together

### Maintenance

1. **Regular Updates**: Update country configuration periodically
2. **Coverage Monitoring**: Check field coverage after major data updates
3. **Backup Changes**: Keep backups of configuration file changes
4. **Version Control**: Track configuration changes in version control

## Troubleshooting Configuration

### Common Issues

#### Invalid Field Paths
**Error**: `Field path not found: Invalid.Field.text`
**Solution**: Check field paths using coverage analysis tools

#### Profile Not Found
**Error**: `Profile 'invalid_profile' not found`
**Solution**: Verify profile name exists in `config/field_profiles.yaml`

#### Country Code Issues
**Error**: `Country code 'xx' not found`
**Solution**: Add country to `config/countries.yaml` or verify code exists in data source

#### YAML Syntax Errors
**Error**: `Invalid YAML syntax`
**Solution**: Validate YAML syntax using online validators or `python -c "import yaml; yaml.safe_load(open('file.yaml'))"`

### Debugging Configuration

Use verbose mode to see configuration loading details:

```bash
python main.py --verbose --countries us --profile standard
```

This will show:
- Country configuration loading status
- Field profile loading and validation
- Field availability for processed countries
