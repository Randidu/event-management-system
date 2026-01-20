from sqlalchemy.orm import Session, joinedload
from app.models.booking import Booking
from app.schemas.booking_schema import BookingCreate
import qrcode
from pathlib import Path
import uuid
from io import BytesIO

QR_CODE_DIR = Path("uploads/qr_codes")
QR_CODE_DIR.mkdir(parents=True, exist_ok=True)

def generate_qr_code(booking_id: int, event_title: str) -> str:
    qr_data = f"BOOKING-{booking_id}-{event_title}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"booking_{booking_id}_{uuid.uuid4().hex[:8]}.png"
    file_path = QR_CODE_DIR / filename
    img.save(str(file_path))
    
    return f"/uploads/qr_codes/{filename}"

def create_booking(db: Session, booking: BookingCreate, user_id: int):
    from app.models.event import Event
    
    event = db.query(Event).filter(Event.id == booking.event_id).first()
    if not event:
        raise ValueError("Event not found")
    
    price_per_ticket = booking.ticket_price if booking.ticket_price is not None else event.ga_ticket_price
    subtotal = price_per_ticket * booking.quantity
    
    # Calculate Fees (Must match frontend logic)
    service_fee = subtotal * 0.10
    processing_fee = 150.00
    total_price = subtotal + service_fee + processing_fee
    
    new_booking = Booking(
        event_id=booking.event_id,
        user_id=user_id,
        ticket_type=getattr(booking, 'ticket_type', 'General Admission'),
        quantity=booking.quantity,
        total_price=total_price,
        amount_total=total_price,
        status="PENDING",
        payment_status="PENDING"
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    try:
        qr_path = generate_qr_code(new_booking.id, event.title)
        new_booking.qr_code_path = qr_path
        db.commit()
        db.refresh(new_booking)
    except Exception as e:
        print(f"Error generating QR code: {e}")
        # Continue without QR code, don't crash the booking
        pass
    
    return new_booking

def confirm_booking_payment(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        booking.status = "CONFIRMED"
        booking.payment_status = "PAID"
        db.commit()
        db.refresh(booking)
    return booking

def booking_read(db: Session, booking_id: int) -> Booking:
    return db.query(Booking).options(
        joinedload(Booking.event),
        joinedload(Booking.user)
    ).filter(Booking.id == booking_id).first()

def booking_update(db: Session, booking_id: int, update_data: dict) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        for key, value in update_data.items():
            setattr(booking, key, value)
        db.commit()
        db.refresh(booking)
    return booking

def get_bookings_by_event(db: Session, event_id: int):
    return db.query(Booking).options(joinedload(Booking.user)).filter(Booking.event_id == event_id).all()

def get_bookings_by_user(db: Session, user_id: int):
    return db.query(Booking).options(joinedload(Booking.event)).filter(Booking.user_id == user_id).all()

def get_all_bookings(db: Session):
    return db.query(Booking).options(
        joinedload(Booking.event), 
        joinedload(Booking.user)
    ).all()

def delete_booking(db: Session, booking_id: int) -> bool:
    """Delete a booking and return True if successful"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        db.delete(booking)
        db.commit()
        return True
    return False
