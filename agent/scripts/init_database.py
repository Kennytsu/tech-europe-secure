#!/usr/bin/env python3
"""
Database initialization script for drive-thru data pipeline
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from drive_thru.database_config import get_database
from drive_thru.models import Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize the database with all tables"""
    try:
        db = get_database()
        
        # Test connection
        if not db.test_connection():
            logger.error("Database connection failed")
            return False
        
        # Create tables
        logger.info("Creating database tables...")
        db.create_tables()
        
        # Print connection info
        connection_info = db.get_connection_info()
        logger.info(f"Database initialized successfully: {connection_info}")
        
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False


def drop_database():
    """Drop all database tables (use with caution!)"""
    try:
        db = get_database()
        
        logger.warning("Dropping all database tables...")
        db.drop_tables()
        
        logger.info("Database tables dropped successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database drop failed: {e}")
        return False


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Drive-Thru Database Management")
    parser.add_argument("--init", action="store_true", help="Initialize database")
    parser.add_argument("--drop", action="store_true", help="Drop all tables (DANGEROUS)")
    parser.add_argument("--test", action="store_true", help="Test database connection")
    
    args = parser.parse_args()
    
    if args.drop:
        if input("Are you sure you want to drop all tables? (yes/no): ").lower() == 'yes':
            success = drop_database()
        else:
            logger.info("Operation cancelled")
            success = True
    elif args.init:
        success = init_database()
    elif args.test:
        db = get_database()
        success = db.test_connection()
        if success:
            logger.info("Database connection test successful")
        else:
            logger.error("Database connection test failed")
    else:
        parser.print_help()
        success = True
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
