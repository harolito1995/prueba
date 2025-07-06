from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String, unique=True, index=True, nullable=False)
    created_date = Column(DateTime, default=func.now())
    
    # Relationship
    processing_results = relationship("ProcessingResult", back_populates="device")

class ProcessingResult(Base):
    __tablename__ = "processing_results"
    
    id = Column(String, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    average_before_normalization = Column(Float, nullable=False)
    average_after_normalization = Column(Float, nullable=False)
    data_size = Column(Integer, nullable=False)
    raw_data = Column(JSON, nullable=False)  # Store original data
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship
    device = relationship("Device", back_populates="processing_results")