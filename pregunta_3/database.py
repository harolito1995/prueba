from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration - PostgreSQL with proper encoding
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/medical_db"
)

# Add connection parameters to fix UTF-8 encoding issues
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "options": "-c client_encoding=utf8",
        "application_name": "medical_api"
    } if DATABASE_URL.startswith("postgresql") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()