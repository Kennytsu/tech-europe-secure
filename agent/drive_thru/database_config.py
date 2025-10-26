"""
Database configuration and connection management
"""
import os
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import asynccontextmanager
import logging
from .models import Base

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration and connection management"""
    
    def __init__(self):
        self.database_url = self._get_database_url()
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()
    
    def _get_database_url(self) -> str:
        """Get database URL from environment variables"""
        # For development, use SQLite. For production, use PostgreSQL
        db_type = os.getenv("DATABASE_TYPE", "sqlite")
        
        if db_type == "postgresql":
            host = os.getenv("POSTGRES_HOST", "localhost")
            port = os.getenv("POSTGRES_PORT", "5432")
            database = os.getenv("POSTGRES_DB", "drive_thru")
            username = os.getenv("POSTGRES_USER", "postgres")
            password = os.getenv("POSTGRES_PASSWORD", "password")
            
            return f"postgresql://{username}:{password}@{host}:{port}/{database}"
        else:
            # SQLite for development
            db_path = os.getenv("SQLITE_PATH", "drive_thru.db")
            return f"sqlite:///{db_path}"
    
    def _initialize_engine(self):
        """Initialize SQLAlchemy engine with appropriate settings"""
        try:
            if self.database_url.startswith("sqlite"):
                # SQLite configuration
                self.engine = create_engine(
                    self.database_url,
                    echo=False,  # Set to True for SQL debugging
                    pool_pre_ping=True,
                )
            else:
                # PostgreSQL configuration
                self.engine = create_engine(
                    self.database_url,
                    echo=False,
                    poolclass=QueuePool,
                    pool_size=10,
                    max_overflow=20,
                    pool_pre_ping=True,
                    pool_recycle=3600,
                )
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info(f"Database engine initialized: {self.database_url.split('@')[-1] if '@' in self.database_url else self.database_url}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all database tables (use with caution!)"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get a new database session"""
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized")
        return self.SessionLocal()
    
    @asynccontextmanager
    async def get_async_session(self):
        """Get an async database session context manager"""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
                logger.info("Database connection test successful")
                return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def get_connection_info(self) -> dict:
        """Get database connection information"""
        return {
            "database_url": self.database_url.split('@')[-1] if '@' in self.database_url else self.database_url,
            "engine_type": "PostgreSQL" if "postgresql" in self.database_url else "SQLite",
            "pool_size": getattr(self.engine.pool, 'size', 'N/A') if hasattr(self.engine, 'pool') else 'N/A',
            "max_overflow": getattr(self.engine.pool, 'max_overflow', 'N/A') if hasattr(self.engine, 'pool') else 'N/A',
        }


# Global database instance
db_config = DatabaseConfig()


def get_database() -> DatabaseConfig:
    """Get the global database configuration instance"""
    return db_config


def get_db_session() -> Session:
    """Get a database session (dependency injection for FastAPI)"""
    session = db_config.get_session()
    try:
        yield session
    finally:
        session.close()


# Database health check
def check_database_health() -> dict:
    """Check database health and return status"""
    try:
        is_connected = db_config.test_connection()
        connection_info = db_config.get_connection_info()
        
        return {
            "status": "healthy" if is_connected else "unhealthy",
            "connected": is_connected,
            "connection_info": connection_info,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "connected": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
