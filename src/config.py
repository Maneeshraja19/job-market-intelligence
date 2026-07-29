import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

def check_credentials():
    """Verify that API credentials are loaded correctly."""
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise ValueError("Missing Adzuna API credentials. Check your .env file.")
    print("Adzuna credentials loaded successfully.")

if __name__ == "__main__":
    check_credentials()