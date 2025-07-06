from pydantic import BaseModel, validator, Field
from typing import List, Optional
from datetime import datetime

class ProcessingResultCreate(BaseModel):
    id: str = Field(..., min_length=1, description="Unique identifier for the processing result")
    data: List[str] = Field(..., min_items=1, description="List of data rows, each containing space-separated numbers")
    device_name: str = Field(..., min_length=1, description="Name of the device that generated the data")
    
    @validator('data')
    def validate_data(cls, v):
        """Validate that data contains only valid numbers"""
        if not v:
            raise ValueError("Data list cannot be empty")
        
        for i, row in enumerate(v):
            if not row.strip():
                raise ValueError(f"Row {i+1} cannot be empty")
            
            numbers = row.split()
            if not numbers:
                raise ValueError(f"Row {i+1} must contain at least one number")
            
            for j, num_str in enumerate(numbers):
                try:
                    float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number '{num_str}' in row {i+1}, position {j+1}")
        
        return v
    
    @validator('device_name')
    def validate_device_name(cls, v):
        """Validate device name"""
        if not v.strip():
            raise ValueError("Device name cannot be empty")
        return v.strip()

class ProcessingResultUpdate(BaseModel):
    device_name: Optional[str] = None
    id: Optional[str] = None

class DeviceResponse(BaseModel):
    id: int
    device_name: str
    created_date: datetime
    
    class Config:
        from_attributes = True

class ProcessingResultResponse(BaseModel):
    id: str
    device_id: int
    average_before_normalization: float
    average_after_normalization: float
    data_size: int
    created_date: datetime
    updated_date: datetime
    device: DeviceResponse
    
    class Config:
        from_attributes = True