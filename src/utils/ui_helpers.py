"""
UI Helpers for CIA Factbook JSON to Excel Exporter.

Provides centralized visual feedback utilities using Rich and tqdm
for consistent and professional CLI appearance.
"""

from rich.console import Console
from tqdm import tqdm

# Global console instance for consistent styling
console = Console()


def print_success(message: str):
    """Print success message in green"""
    console.print(f"✓ {message}", style="green")


def print_error(message: str):
    """Print error message in red"""
    console.print(f"✗ {message}", style="red")


def print_warning(message: str):
    """Print warning message in yellow"""
    console.print(f"⚠ {message}", style="yellow")


def print_info(message: str):
    """Print info message in blue"""
    console.print(f"ℹ {message}", style="blue")


def create_progress_bar(total: int, description: str):
    """
    Create a progress bar for tracking operations.
    
    Args:
        total: Total number of items to process
        description: Description text for the progress bar
        
    Returns:
        tqdm progress bar instance
    """
    return tqdm(
        total=total,
        desc=description,
        unit="country",
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
    )
