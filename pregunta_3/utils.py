import logging
from typing import List, Any
import statistics

def setup_logging(log_level: str = "INFO", log_file: str = "api.log") -> logging.Logger:
    """Setup logging configuration"""
    logger = logging.getLogger("medical_api")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def validate_numeric_data(data: List[str]) -> bool:
    """Validate that all data contains only numbers"""
    try:
        for row in data:
            numbers = row.split()
            for num_str in numbers:
                float(num_str)
        return True
    except (ValueError, AttributeError):
        return False

def normalize_data(data: List[str]) -> tuple[List[float], float, float]:
    """
    Normalize data to 0-1 scale and return statistics
    
    Returns:
        tuple: (normalized_data, avg_before, avg_after)
    """
    # Convert to numbers
    all_numbers = []
    for row in data:
        numbers = [float(x) for x in row.split()]
        all_numbers.extend(numbers)
    
    # Calculate statistics before normalization
    avg_before = statistics.mean(all_numbers)
    
    # Normalize (0 to 1)
    max_value = max(all_numbers) if all_numbers else 1
    normalized_numbers = [x / max_value for x in all_numbers]
    
    # Calculate statistics after normalization
    avg_after = statistics.mean(normalized_numbers)
    
    return normalized_numbers, avg_before, avg_after

def calculate_data_size(data: List[str]) -> int:
    """Calculate total number of data points"""
    total = 0
    for row in data:
        total += len(row.split())
    return total
