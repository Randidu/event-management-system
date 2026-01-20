from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WishlistItemCreate(BaseModel):
    user_id: int
    event_id: int

class EventSummary(BaseModel):
    id: int
    title: str
    location: str
    starts_at: datetime
    ga_ticket_price: Optional[float] = None
    
    class Config:
        from_attributes = True

class WishlistItemRead(BaseModel):
    id: int
    user_id: int
    event_id: int
    added_at: datetime
    event: EventSummary

    class Config:
        from_attributes = True
