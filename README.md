# CIA Factbook Exporter

Extract country data from CIA World Factbook to Excel.

## Quick Start

```bash
git clone <repository>
cd factbook_exporter
source ./activate.sh
```

The setup script will automatically:
- Create a Python virtual environment
- Install all required dependencies  
- Activate the virtual environment
- Guide you through running the application

**Note**: Use `source ./activate.sh` (or `./activate.sh` for temporary activation) to keep the virtual environment active after setup.

## Usage

```bash
# Interactive mode
python main.py --interactive

# Specific countries with profile
python main.py --countries fr,de,pl --profile economy

# List available profiles
python main.py --list-profiles
```

## Key Features

- Export 250+ countries from CIA World Factbook
- Configurable field profiles (minimal, standard, geography, economy, comprehensive)
- Clean Excel output with formatted data
- Interactive and command-line interfaces

## Documentation

- **Usage Guide**: [docs/USAGE.md](docs/USAGE.md)
- **Configuration**: [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
- **Technical Details**: [docs/TECHNICAL.md](docs/TECHNICAL.md)

## Requirements

- Python 3.11+
- Internet connection (fetches data from GitHub)

## License

This project is provided as-is for educational and research purposes.

## Data Source Attribution

Country data sourced from the CIA World Factbook, maintained by the U.S. Central Intelligence Agency.
Repository: https://github.com/factbook/factbook.json
