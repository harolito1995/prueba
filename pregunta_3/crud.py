from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
import statistics

from models import ProcessingResult, Device
from schemas import ProcessingResultCreate, ProcessingResultUpdate

def get_or_create_device(db: Session, device_name: str) -> Device:
    """Get existing device or create new one"""
    device = db.query(Device).filter(Device.device_name == device_name).first()
    if not device:
        device = Device(device_name=device_name)
        db.add(device)
        db.commit()
        db.refresh(device)
    return device

def process_data(data: List[str]) -> tuple:
    """Process raw data and return statistics"""
    # Convert string data to numbers
    all_numbers = []
    for row in data:
        numbers = [float(x) for x in row.split()]
        all_numbers.extend(numbers)
    
    # Calculate average before normalization
    avg_before = statistics.mean(all_numbers)
    
    # Normalize data (0 to 1)
    max_value = max(all_numbers)
    normalized_numbers = [x / max_value for x in all_numbers]
    
    # Calculate average after normalization
    avg_after = statistics.mean(normalized_numbers)
    
    return avg_before, avg_after, len(all_numbers)

def create_processing_result(db: Session, result: ProcessingResultCreate) -> ProcessingResult:
    """Create a new processing result"""
    # Get or create device
    device = get_or_create_device(db, result.device_name)
    
    # Process data
    avg_before, avg_after, data_size = process_data(result.data)
    
    # Create processing result
    db_result = ProcessingResult(
        id=result.id,
        device_id=device.id,
        average_before_normalization=avg_before,
        average_after_normalization=avg_after,
        data_size=data_size,
        raw_data=result.data
    )
    
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_processing_results(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    **filters
) -> List[ProcessingResult]:
    """Get processing results with optional filtering"""
    query = db.query(ProcessingResult)
    
    # Apply filters
    if filters.get('created_date_from'):
        query = query.filter(ProcessingResult.created_date >= filters['created_date_from'])
    if filters.get('created_date_to'):
        query = query.filter(ProcessingResult.created_date <= filters['created_date_to'])
    if filters.get('updated_date_from'):
        query = query.filter(ProcessingResult.updated_date >= filters['updated_date_from'])
    if filters.get('updated_date_to'):
        query = query.filter(ProcessingResult.updated_date <= filters['updated_date_to'])
    if filters.get('avg_before_min'):
        query = query.filter(ProcessingResult.average_before_normalization >= filters['avg_before_min'])
    if filters.get('avg_before_max'):
        query = query.filter(ProcessingResult.average_before_normalization <= filters['avg_before_max'])
    if filters.get('avg_after_min'):
        query = query.filter(ProcessingResult.average_after_normalization >= filters['avg_after_min'])
    if filters.get('avg_after_max'):
        query = query.filter(ProcessingResult.average_after_normalization <= filters['avg_after_max'])
    if filters.get('data_size_min'):
        query = query.filter(ProcessingResult.data_size >= filters['data_size_min'])
    if filters.get('data_size_max'):
        query = query.filter(ProcessingResult.data_size <= filters['data_size_max'])
    
    return query.offset(skip).limit(limit).all()

def get_processing_result(db: Session, result_id: str) -> Optional[ProcessingResult]:
    """Get a specific processing result by ID"""
    return db.query(ProcessingResult).filter(ProcessingResult.id == result_id).first()

def update_processing_result(
    db: Session,
    result_id: str,
    update_data: ProcessingResultUpdate
) -> Optional[ProcessingResult]:
    """Update a processing result"""
    db_result = db.query(ProcessingResult).filter(ProcessingResult.id == result_id).first()
    if not db_result:
        return None
    
    # Update device if provided
    if update_data.device_name:
        device = get_or_create_device(db, update_data.device_name)
        db_result.device_id = device.id
    
    # Update ID if provided
    if update_data.id:
        db_result.id = update_data.id
    
    db.commit()
    db.refresh(db_result)
    return db_result

def delete_processing_result(db: Session, result_id: str) -> bool:
    """Delete a processing result"""
    db_result = db.query(ProcessingResult).filter(ProcessingResult.id == result_id).first()
    if not db_result:
        return False
    
    db.delete(db_result)
    db.commit()
    return True
