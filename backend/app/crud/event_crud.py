from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models import Event, EventStatus, Category
from app.schemas.event_schema import EventCreate, EventUpdate

def create_event(db: Session, event: EventCreate) -> Event:
    db_event = Event(
        title=event.title,
        description=event.description,
        category=event.category,
        status=event.status or EventStatus.DRAFT.value,
        location=event.location,
        starts_at=event.starts_at,
        ends_at=event.ends_at,
        capacity=event.capacity,
        organizer_id=event.organizer_id,
        ga_ticket_price=event.ga_ticket_price or 0.0,
        vip_ticket_price=event.vip_ticket_price or 0.0,
        pa_ticket_price=event.pa_ticket_price or 0.0,
        poster_url=event.poster_url,  # Added poster_url
    )
    db.add(db_event)
    db.commit() 
    db.refresh(db_event)
    return db_event

def list_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    return db.query(Event).offset(skip).limit(limit).all()

def get_event(db: Session, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()

def get_events(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    status: Optional[EventStatus] = None,
    category: Optional[Category] = None
) -> List[Event]:
    query = db.query(Event)
    
    if status:
        query = query.filter(Event.status == status.value)
    
    if category:
        query = query.filter(Event.category == category.value)
    
    return query.offset(skip).limit(limit).all()

def update_event(db: Session, event_id: int, updated_event: EventUpdate) -> Optional[Event]:
    db_event = get_event(db, event_id)
    if not db_event:
        return None
    
    # Update only non-None fields
    update_data = updated_event.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int) -> bool:
    db_event = get_event(db, event_id)
    if not db_event:
        return False
    
    db.delete(db_event)
    db.commit()
    return True

def get_events_by_organizer(db: Session, organizer_id: int) -> List[Event]:
    return db.query(Event).filter(Event.organizer_id == organizer_id).all()

def get_upcoming_events(db: Session, current_time: datetime) -> List[Event]:
    return db.query(Event).filter(
        Event.starts_at > current_time,
        Event.status != EventStatus.CANCELLED.value
    ).order_by(Event.starts_at.asc()).all()

def get_past_events(db: Session, current_time: datetime) -> List[Event]:
    return db.query(Event).filter(
        Event.ends_at < current_time
    ).order_by(Event.ends_at.desc()).all()

def get_events_by_location(db: Session, location: str) -> List[Event]:
    return db.query(Event).filter(
        Event.location.ilike(f"%{location}%")
    ).all()

def get_events_by_date_range(db: Session, start_date: datetime, end_date: datetime) -> List[Event]:
    return db.query(Event).filter(
        Event.starts_at >= start_date,
        Event.ends_at <= end_date
    ).order_by(Event.starts_at.asc()).all()

def get_events_by_capacity(db: Session, min_capacity: int, max_capacity: int) -> List[Event]:
    return db.query(Event).filter(
        Event.capacity >= min_capacity,
        Event.capacity <= max_capacity
    ).all()

def get_events_by_title_keyword(db: Session, keyword: str) -> List[Event]:
    return db.query(Event).filter(
        Event.title.ilike(f"%{keyword}%")
    ).all()

def get_published_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    return db.query(Event).filter(
        Event.status == EventStatus.PUBLISHED.value
    ).offset(skip).limit(limit).all()

def get_events_count(db: Session) -> int:
    return db.query(Event).count()

def get_events_by_status_count(db: Session, status: EventStatus) -> int:
    return db.query(Event).filter(Event.status == status.value).count()