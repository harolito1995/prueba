from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from contextlib import asynccontextmanager
from pydantic import ValidationError

from database import SessionLocal, engine, Base
from models import Device, ProcessingResult
from schemas import (
    ProcessingResultCreate, ProcessingResultResponse, 
    ProcessingResultUpdate, DeviceResponse
)
from crud import (
    create_processing_result, get_processing_results,
    get_processing_result, update_processing_result,
    delete_processing_result
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Medical Image Processing API",
    description="API for managing medical image processing results",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response
    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(f"Response: {response.status_code} - Time: {process_time:.4f}s")
    
    return response

@app.post("/api/elements/", response_model=List[ProcessingResultResponse])
async def create_elements(
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Create new processing results from JSON payload"""
    try:
        logger.info(f"Creating elements from payload with {len(payload)} items")
        
        results = []
        for key, element in payload.items():
            # Validate required fields
            if not all(field in element for field in ['id', 'data', 'deviceName']):
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required fields in element {key}"
                )
            
            try:
                # Create processing result with validation
                result_data = ProcessingResultCreate(
                    id=element['id'],
                    data=element['data'],
                    device_name=element['deviceName']
                )
                
                result = create_processing_result(db, result_data)
                results.append(result)
                
            except ValidationError as validation_error:
                # Handle Pydantic validation errors specifically
                error_details = []
                for error in validation_error.errors():
                    field = error['loc'][0] if error['loc'] else 'unknown'
                    message = error['msg']
                    error_details.append(f"Field '{field}': {message}")
                
                error_message = f"Validation error in element {key}: {'; '.join(error_details)}"
                logger.warning(f"Validation error: {error_message}")
                raise HTTPException(
                    status_code=422,
                    detail=error_message
                )
        
        logger.info(f"Successfully created {len(results)} processing results")
        return results
        
    except HTTPException:
        # Re-raise HTTP exceptions (including our 422 errors)
        raise
    except IntegrityError as e:
        # Handle database integrity errors (e.g., duplicate keys)
        if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
            logger.warning(f"Duplicate key error: {str(e)}")
            raise HTTPException(
                status_code=409,
                detail="A processing result with this ID already exists"
            )
        else:
            logger.error(f"Database integrity error: {str(e)}")
            raise HTTPException(status_code=500, detail="Database integrity error")
    except Exception as e:
        logger.error(f"Error creating elements: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/elements/", response_model=List[ProcessingResultResponse])
async def get_elements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    created_date_from: Optional[datetime] = None,
    created_date_to: Optional[datetime] = None,
    updated_date_from: Optional[datetime] = None,
    updated_date_to: Optional[datetime] = None,
    avg_before_min: Optional[float] = None,
    avg_before_max: Optional[float] = None,
    avg_after_min: Optional[float] = None,
    avg_after_max: Optional[float] = None,
    data_size_min: Optional[int] = None,
    data_size_max: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all processing results with optional filtering"""
    try:
        logger.info("Retrieving processing results with filters")
        
        filters = {
            'created_date_from': created_date_from,
            'created_date_to': created_date_to,
            'updated_date_from': updated_date_from,
            'updated_date_to': updated_date_to,
            'avg_before_min': avg_before_min,
            'avg_before_max': avg_before_max,
            'avg_after_min': avg_after_min,
            'avg_after_max': avg_after_max,
            'data_size_min': data_size_min,
            'data_size_max': data_size_max,
        }
        
        results = get_processing_results(db, skip=skip, limit=limit, **filters)
        logger.info(f"Retrieved {len(results)} processing results")
        return results
        
    except Exception as e:
        logger.error(f"Error retrieving elements: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/elements/{element_id}", response_model=ProcessingResultResponse)
async def get_element(element_id: str, db: Session = Depends(get_db)):
    """Get a specific processing result by ID"""
    try:
        logger.info(f"Retrieving processing result with ID: {element_id}")
        
        result = get_processing_result(db, element_id)
        if not result:
            raise HTTPException(status_code=404, detail="Processing result not found")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving element {element_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/elements/{element_id}", response_model=ProcessingResultResponse)
async def update_element(
    element_id: str,
    update_data: ProcessingResultUpdate,
    db: Session = Depends(get_db)
):
    """Update a processing result"""
    try:
        logger.info(f"Updating processing result with ID: {element_id}")
        
        result = update_processing_result(db, element_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail="Processing result not found")
        
        logger.info(f"Successfully updated processing result {element_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating element {element_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/elements/{element_id}")
async def delete_element(element_id: str, db: Session = Depends(get_db)):
    """Delete a processing result"""
    try:
        logger.info(f"Deleting processing result with ID: {element_id}")
        
        success = delete_processing_result(db, element_id)
        if not success:
            raise HTTPException(status_code=404, detail="Processing result not found")
        
        logger.info(f"Successfully deleted processing result {element_id}")
        return {"message": "Processing result deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting element {element_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)