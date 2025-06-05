from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection settings

# Prioritize reading from DATABASE_URL environment variable (used by Render)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Fallback to individual variables (for local development)
    DB_USER = os.getenv("DB_USER", "snakegame")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "snakegame123")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "swipe_melody")
    
    # Note: If using individual variables locally with a different DB type (like MySQL), adjust this format.
    # For PostgreSQL locally, you might need a URL like: postgresql://user:password@host:port/dbname
    # Assuming for now this fallback is primarily for local testing with the original setup if needed.
    SQLALCHEMY_DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 