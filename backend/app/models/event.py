from __future__ import annotations
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .user import User
    from .booking import Booking
    from .wishlist import WishlistItem

class EventStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class Category(str, Enum):
    CONFERENCE = "CONFERENCE"
    CONCERT = "CONCERT"
    WORKSHOP = "WORKSHOP"
    SPORTS = "SPORTS"
    MEETUP = "MEETUP"
    OTHER = "OTHER"

class Event(Base):
    __tablename__ = "events"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Event Details
    poster_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[Category] = mapped_column(String(30))
    status: Mapped[EventStatus] = mapped_column(String(20), default=EventStatus.DRAFT.value)
    location: Mapped[str] = mapped_column(String(250))
    
    # Dates
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    # Capacity
    capacity: Mapped[int] = mapped_column(Integer)
    
    # Foreign Key
    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Ticket Prices
    ga_ticket_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)
    vip_ticket_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)
    pa_ticket_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)

    # Relationships
    organizer: Mapped["User"] = relationship("User", back_populates="events")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="event", cascade="all, delete-orphan")
    wishlist_items: Mapped[list["WishlistItem"]] = relationship("WishlistItem", back_populates="event", cascade="all, delete-orphan")