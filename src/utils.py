import os
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
import logging

# Initialize console for rich output
console = Console()

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("slidesgpt")

def get_api_key() -> str:
    """Get the Google API key from environment variables"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please create a .env file with your API key.")
    return api_key

def ensure_output_dir(output_path: str) -> None:
    """Ensure the output directory exists"""
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True) 