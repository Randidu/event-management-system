from __future__ import annotations
from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from .event import Event
    from .booking import Booking
    from .wishlist import WishlistItem
    from .ticket import Ticket, TicketComment

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    role: Mapped[UserRole] = mapped_column(String(20))
    profile_image: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    events: Mapped[list["Event"]] = relationship("Event", back_populates="organizer", cascade="all, delete-orphan")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    wishlist_items: Mapped[list["WishlistItem"]] = relationship("WishlistItem", back_populates="user", cascade="all, delete-orphan")
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", foreign_keys="[Ticket.requester_id]", back_populates="requester")
    assigned_tickets: Mapped[list["Ticket"]] = relationship("Ticket", foreign_keys="[Ticket.assignee_id]", back_populates="assignee")
    ticket_comments: Mapped[list["TicketComment"]] = relationship("TicketComment", back_populates="author")

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"