import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/medical_db"
    
    # API
    api_title: str = "Medical Image Processing API"
    api_version: str = "1.0.0"
    api_description: str = "API for managing medical image processing results"
    
    # Security
    allowed_origins: list = ["*"]
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "api.log"
    
    # Pagination
    default_page_size: int = 100
    max_page_size: int = 1000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()