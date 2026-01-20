from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum

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

class BookingBase(BaseModel):
    event_id: int = Field(..., gt=0, description="ID of the event to book")
    quantity: int = Field(..., gt=0, le=20, description="Number of tickets (1-20)")

    attendee_name: Optional[str] = Field(None, max_length=100, description="Attendee name")
    attendee_email: Optional[str] = Field(None, max_length=100, description="Attendee email")
    attendee_phone: Optional[str] = Field(None, max_length=20, description="Attendee phone")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")

    @validator("quantity")
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        if v > 20:
            raise ValueError("Cannot book more than 20 tickets at once")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": 1,
                "quantity": 2,
                "attendee_name": "John Doe",
                "attendee_email": "john@example.com",
                "attendee_phone": "+94771234567",
                "notes": "Vegetarian meal preference",
            }
        }
    }

class BookingCreate(BookingBase):
    ticket_type: Optional[str] = Field(None, max_length=50, description="Type of ticket")
    ticket_price: Optional[float] = Field(None, ge=0, description="Price per ticket")

class BookingRead(BaseModel):
    id: int
    user_id: int
    event_id: int
    ticket_type: Optional[str] = None
    quantity: int
    total_price: Optional[float] = None
    amount_total: float
    currency: str = "LKR"
    status: str = "PENDING"
    payment_status: str = "PENDING"
    qr_code_path: Optional[str] = None
    booked_at: datetime

    attendee_name: Optional[str] = None
    attendee_email: Optional[str] = None
    attendee_phone: Optional[str] = None
    notes: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 123,
                "event_id": 456,
                "quantity": 2,
                "amount_total": 5000.00,
                "currency": "LKR",
                "status": "CONFIRMED",
                "payment_status": "PAID",
                "booked_at": "2025-01-11T10:30:00",
                "attendee_name": "John Doe",
                "attendee_email": "john@example.com",
                "attendee_phone": "+94771234567",
                "notes": "Window seat preferred",
            }
        },
    }

class BookingUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0, le=20)
    status: Optional[BookingStatus] = None
    payment_status: Optional[PaymentStatus] = None
    attendee_name: Optional[str] = Field(None, max_length=100)
    attendee_email: Optional[str] = Field(None, max_length=100)
    attendee_phone: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = Field(None, max_length=500)

    @validator("quantity")
    def validate_quantity(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("Quantity must be greater than 0")
            if v > 20:
                raise ValueError("Cannot book more than 20 tickets at once")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {"status": "CONFIRMED", "payment_status": "PAID"}
        }
    }

class EventSummary(BaseModel):
    id: int
    title: str
    starts_at: datetime
    poster_url: Optional[str] = None
    location: Optional[str] = None
    
    # We can keep these if strictly needed, but model has 'location' string
    # venue_name: Optional[str] = None 
    # city: Optional[str] = None
    
    # price was problematic as Event has multiple prices. 
    # If we need a 'price', we might need to compute it or alias it.
    # For now, let's include generic 'ga_ticket_price' as 'price' or just omit if not used by ticket_list
    # ticket_list.html doesn't seem to use event.price, only booking.amount_total
    
    model_config = {"from_attributes": True}

class UserSummary(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    
    # helper for frontend if needed, but easier to just send first/last
    @validator("phone", pre=True, check_fields=False)
    def map_phone(cls, v, values):
        return v or values.get("phone_number")

    model_config = {"from_attributes": True}

class BookingWithDetails(BookingRead):
    event: Optional[EventSummary] = None
    user: Optional[UserSummary] = None

    model_config = {"from_attributes": True}

class BookingStatusUpdate(BaseModel):
    status: BookingStatus

    model_config = {
        "json_schema_extra": {"example": {"status": "CONFIRMED"}}
    }

class PaymentStatusUpdate(BaseModel):
    payment_status: PaymentStatus

    model_config = {
        "json_schema_extra": {"example": {"payment_status": "PAID"}}
    }

class BookingCancellation(BaseModel):
    reason: Optional[str] = Field(None, max_length=500)
    request_refund: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {"reason": "Unable to attend", "request_refund": True}
        }
    }

class BookingResponse(BaseModel):
    success: bool
    message: str
    booking: Optional[BookingRead] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Booking created successfully",
                "booking": None,
            }
        }
    }

class BookingError(BaseModel):
    error: bool = True
    message: str
    error_code: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": True,
                "message": "Not enough seats available",
                "error_code": "INSUFFICIENT_SEATS",
            }
        }
    }