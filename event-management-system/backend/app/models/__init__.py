"""
Models package initialization.
Import all models here to ensure they're registered with SQLAlchemy
before any relationships are configured.
"""

# Import Base first
from app.core.database import Base

# Import all models in dependency order
# User has no dependencies, import first
from .user import User, UserRole

# Event depends on User
from .event import Event, EventStatus, Category

# Booking depends on User and Event
from .booking import Booking, BookingStatus, PaymentStatus

# WishlistItem depends on User and Event
from .wishlist import WishlistItem

# Ticket depends on User
from .ticket import Ticket, TicketComment, TicketStatus

# Export all models
__all__ = [
    "Base",
    "User",
    "UserRole",
    "Event",
    "EventStatus",
    "Category",
    "Booking",
    "BookingStatus",
    "PaymentStatus",
    "WishlistItem",
    "Ticket",
    "TicketComment",
    "TicketStatus",
]