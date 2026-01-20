from __future__ import annotations
from datetime import datetime
from enum import Enum
from sqlalchemy import ForeignKey, Integer, String, DateTime, Numeric, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from .user import User
    from .event import Event

class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

class PaymentStatus(str, Enum):
    UNPAID = "UNPAID"
    PAID = "PAID"
    PARTIAL = "PARTIAL"
    REFUNDED = "REFUNDED"

class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), index=True)
    ticket_type: Mapped[str] = mapped_column(String(50), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    amount_total: Mapped[float] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    status: Mapped[BookingStatus] = mapped_column(String(20), default=BookingStatus.PENDING.value)
    payment_status: Mapped[str] = mapped_column(String(20), default="PENDING")
    qr_code_path: Mapped[str] = mapped_column(Text, nullable=True)
    booked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="bookings")
    event: Mapped["Event"] = relationship("Event", back_populates="bookings")

    @property
    def is_confirmed(self) -> bool:
        return self.status == BookingStatus.CONFIRMED.value and self.payment_status in {
            PaymentStatus.PAID.value, PaymentStatus.PARTIAL.value
        }