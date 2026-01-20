from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import shutil
import os
import uuid
from pathlib import Path
from app.core.database import get_db
from app.crud import event_crud
from app.schemas.event_schema import EventCreate, EventUpdate, EventResponse
from app.models import EventStatus, Category
import json



router = APIRouter(prefix="/events", tags=["events"])


# Resolve backend root directory (3 levels up from routes/events.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads" / "event_posters"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(
    poster_image: UploadFile = File(None),
    event_data: str = Form(...),
    db: Session = Depends(get_db)
):
    
    try:
        event_dict = json.loads(event_data)
        # Handle image upload if provided
        poster_url = None
        if poster_image and poster_image.filename:
            # Validate file type
            allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
            file_extension = os.path.splitext(poster_image.filename)[1].lower()
            
            if file_extension not in allowed_extensions:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
                )
            
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = UPLOAD_DIR / unique_filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(poster_image.file, buffer)
            
            # Store relative URL
            poster_url = f"/uploads/event_posters/{unique_filename}"
        
        # Add poster_url to event data
        event_dict['poster_url'] = poster_url
        
        # Create event object
        event = EventCreate(**event_dict)
        
        # Save to database
        return event_crud.create_event(db, event)
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[EventResponse])
def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[EventStatus] = None,
    category: Optional[Category] = None,
    db: Session = Depends(get_db)):
    events = event_crud.get_events(db, skip, limit, status, category)
    return events

@router.get("/upcoming", response_model=List[EventResponse])
def get_upcoming_events(db: Session = Depends(get_db)):
    current_time = datetime.utcnow()
    events = event_crud.get_upcoming_events(db, current_time)
    return events

@router.get("/past", response_model=List[EventResponse])
def get_past_events(db: Session = Depends(get_db)):
    current_time = datetime.utcnow()
    events = event_crud.get_past_events(db, current_time)
    return events

@router.get("/search/location", response_model=List[EventResponse])
def search_events_by_location(
    location: str = Query(..., min_length=1),
    db: Session = Depends(get_db)):
    events = event_crud.get_events_by_location(db, location)
    return events

@router.get("/search/title", response_model=List[EventResponse])
def search_events_by_title(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db)):
    events = event_crud.get_events_by_title_keyword(db, keyword)
    return events

@router.get("/search/date-range", response_model=List[EventResponse])
def get_events_by_date_range(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: Session = Depends(get_db)):
    if start_date >= end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
    
    events = event_crud.get_events_by_date_range(db, start_date, end_date)
    return events

@router.get("/search/capacity", response_model=List[EventResponse])
def get_events_by_capacity(
    min_capacity: int = Query(..., ge=0),
    max_capacity: int = Query(..., ge=1),
    db: Session = Depends(get_db)):
    if min_capacity > max_capacity:
        raise HTTPException(status_code=400, detail="min_capacity must be less than or equal to max_capacity")
    
    events = event_crud.get_events_by_capacity(db, min_capacity, max_capacity)
    return events

@router.get("/organizer/{organizer_id}", response_model=List[EventResponse])
def get_events_by_organizer(
    organizer_id: int,
    db: Session = Depends(get_db)):
    events = event_crud.get_events_by_organizer(db, organizer_id)
    return events

@router.get("/{event_id}", response_model=EventResponse)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = event_crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    poster_image: UploadFile = File(None),
    event_data: str = Form(None),
    db: Session = Depends(get_db)):
    import json
    
    existing_event = event_crud.get_event(db, event_id)
    if not existing_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    
    update_dict = {}
    if event_data:
        try:
            update_dict = json.loads(event_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON data")
    
    # Handle new image upload
    if poster_image and poster_image.filename:
        # Delete old image if exists
        if existing_event.poster_url:
            # Clean up path helper
            clean_path = existing_event.poster_url.lstrip("/")
            # If it starts with 'uploads/', we can try to locate it in BASE_DIR/uploads
            if clean_path.startswith("uploads/"):
                old_file_path = BASE_DIR / clean_path
                if old_file_path.exists():
                    old_file_path.unlink()
        
        # Save new image
        file_extension = os.path.splitext(poster_image.filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(poster_image.file, buffer)
        
        update_dict['poster_url'] = f"/uploads/event_posters/{unique_filename}"
    
    # Update event
    updated_event = EventUpdate(**update_dict)
    event = event_crud.update_event(db, event_id, updated_event)
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    # Get event to delete image
    event = event_crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Delete image file if exists
    if event.poster_url:
        clean_path = event.poster_url.lstrip("/")
        if clean_path.startswith("uploads/"):
            file_path = BASE_DIR / clean_path
            if file_path.exists():
                file_path.unlink()
    
    # Delete event from database
    success = event_crud.delete_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")

from app.schemas import booking_schema as import_booking_schema

@router.get("/{event_id}/participants", response_model=List[import_booking_schema.BookingWithDetails])
def get_event_participants(event_id: int, db: Session = Depends(get_db)):
    from app.crud.booking_crud import get_bookings_by_event
    bookings = get_bookings_by_event(db, event_id)
    return bookings