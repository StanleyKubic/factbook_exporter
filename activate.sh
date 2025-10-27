#!/bin/bash
# Smart setup and activation script for the factbook_exporter virtual environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check Python version
check_python_version() {
    print_info "Checking Python version..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed or not in PATH"
        exit 1
    fi
    
    # Get Python version
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    
    # Check if version is 3.11 or higher
    if $PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
        print_success "Python $PYTHON_VERSION found (compatible)"
    else
        print_error "Python $PYTHON_VERSION found, but Python 3.11+ is required"
        exit 1
    fi
}

# Function to create virtual environment
create_venv() {
    print_info "Creating virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment directory already exists. Removing it..."
        rm -rf venv
    fi
    
    $PYTHON_CMD -m venv venv
    
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created successfully"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
}

# Function to activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_success "Virtual environment activated"
    else
        print_error "Virtual environment activation script not found"
        exit 1
    fi
}

# Function to upgrade pip
upgrade_pip() {
    print_info "Upgrading pip..."
    pip install --upgrade pip
    if [ $? -eq 0 ]; then
        print_success "Pip upgraded successfully"
    else
        print_warning "Failed to upgrade pip (continuing anyway)"
    fi
}

# Function to install dependencies
install_dependencies() {
    print_info "Installing dependencies from requirements.txt..."
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_success "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        exit 1
    fi
}

# Function to verify installation
verify_installation() {
    print_info "Verifying key package installations..."
    
    local failed_packages=()
    
    # Check each package individually
    if python -c "import requests" &> /dev/null; then
        print_success "✓ requests"
    else
        print_error "✗ requests"
        failed_packages+=("requests")
    fi
    
    if python -c "import pandas" &> /dev/null; then
        print_success "✓ pandas"
    else
        print_error "✗ pandas"
        failed_packages+=("pandas")
    fi
    
    if python -c "import openpyxl" &> /dev/null; then
        print_success "✓ openpyxl"
    else
        print_error "✗ openpyxl"
        failed_packages+=("openpyxl")
    fi
    
    if python -c "import yaml" &> /dev/null; then
        print_success "✓ pyyaml"
    else
        print_error "✗ pyyaml"
        failed_packages+=("pyyaml")
    fi
    
    if python -c "import tqdm" &> /dev/null; then
        print_success "✓ tqdm"
    else
        print_error "✗ tqdm"
        failed_packages+=("tqdm")
    fi
    
    if python -c "import click" &> /dev/null; then
        print_success "✓ click"
    else
        print_error "✗ click"
        failed_packages+=("click")
    fi
    
    if python -c "import rich" &> /dev/null; then
        print_success "✓ rich"
    else
        print_error "✗ rich"
        failed_packages+=("rich")
    fi
    
    if python -c "import bs4" &> /dev/null; then
        print_success "✓ beautifulsoup4"
    else
        print_error "✗ beautifulsoup4"
        failed_packages+=("beautifulsoup4")
    fi
    
    if python -c "import lxml" &> /dev/null; then
        print_success "✓ lxml"
    else
        print_error "✗ lxml"
        failed_packages+=("lxml")
    fi
    
    if [ ${#failed_packages[@]} -eq 0 ]; then
        print_success "All packages verified successfully"
    else
        print_error "Failed to install packages: ${failed_packages[*]}"
        exit 1
    fi
}

# Function to show completion message
show_completion_message() {
    echo
    print_info "Setup complete! Virtual environment is ready to use."
    echo
    print_info "Usage examples:"
    echo "  python main.py --interactive"
    echo "  python main.py --countries fr,us,uk"
    echo "  python main.py --list-profiles"
    echo
    print_info "You can now run the application with any of the commands above."
}

# Main execution flow
main() {
    echo "=== CIA Factbook Exporter Setup ==="
    echo
    
    # Check Python version and set PYTHON_CMD
    check_python_version
    
    # Check if we're already in a virtual environment
    if [ -n "$VIRTUAL_ENV" ]; then
        print_warning "You're already in a virtual environment: $VIRTUAL_ENV"
        print_info "Please deactivate first and run this script again"
        exit 1
    fi
    
    # Check if venv exists
    if [ -d "venv" ]; then
        print_info "Virtual environment already exists"
        print_info "Checking if it's properly set up..."
        
        # Try to activate and check if key packages are installed
        if source venv/bin/activate 2>/dev/null && python -c "import requests" 2>/dev/null; then
            print_success "Existing virtual environment is properly set up"
            print_info "Activating virtual environment..."
            # Re-activate the virtual environment for the user's session
            # The temporary activation above was only for verification
            source venv/bin/activate
            print_success "Virtual environment activated"
            # Show completion and return
            show_completion_message
            return
        else
            print_warning "Existing virtual environment appears incomplete"
            print_info "Recreating virtual environment..."
            create_venv
        fi
    else
        # Create new virtual environment
        create_venv
    fi
    
    # Activate virtual environment
    activate_venv
    
    # Upgrade pip
    upgrade_pip
    
    # Install dependencies
    install_dependencies
    
    # Verify installation
    verify_installation
    
    # Show completion message
    show_completion_message
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    # Script is being sourced - this is the correct way for venv activation
    main "$@"
    return $?
else
    # Script is being executed - show different behavior
    print_warning "For persistent virtual environment activation, run: source ./activate.sh"
    print_info "Executing will activate venv temporarily for this session..."
    echo
    main "$@"
fi
