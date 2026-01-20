from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from app.schemas.user_schema import UserBase

class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class TicketBase(BaseModel):
    subject: str
    description: str

class TicketCreate(TicketBase):
    requester_id: int
    assignee_id: int | None = None

class TicketUpdate(BaseModel):
    status: TicketStatus | None = None
    assignee_id: int | None = None

class TicketCommentCreate(BaseModel):
    ticket_id: int
    author_id: int
    body: str

class TicketCommentRead(TicketCommentCreate):
    id: int
    created_at: datetime
    author: UserBase

    class Config:
        orm_mode = True

class TicketRead(TicketBase):
    id: int
    status: TicketStatus
    requester_id: int
    assignee_id: int | None
    created_at: datetime
    updated_at: datetime
    
    requester: UserBase
    assignee: UserBase | None = None
    comments: list[TicketCommentRead] = []

    class Config:
        orm_mode = True
