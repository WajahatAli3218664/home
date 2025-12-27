#!/usr/bin/env python
"""
Database migration setup script for the auth, personalization, and translation system.

This script will create the database tables based on the defined models.
"""

import sys
import os

# Add the backend/src directory to the Python path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.database.models import create_db_and_tables
from src.config.settings import settings


def setup_database():
    """Set up the database by creating all required tables"""
    print("Setting up database...")
    
    try:
        print(f"Using database URL: {settings.database_url}")
        create_db_and_tables()
        print("Database setup completed successfully.")
        return True
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        return False


if __name__ == "__main__":
    success = setup_database()
    if not success:
        sys.exit(1)