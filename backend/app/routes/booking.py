from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.booking_schema import BookingCreate, BookingRead, BookingWithDetails
from app.crud.booking_crud import create_booking, get_bookings_by_user, booking_read, confirm_booking_payment, get_all_bookings, delete_booking
from app.routes.wishlist import get_current_user # Re-using dependency
from app.models.user import User

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingRead)
def create_new_booking(
    booking: BookingCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # TODO: Add logic to check event capacity, etc.
    return create_booking(db, booking, user_id=current_user.id)

@router.post("/{booking_id}/confirm-payment", response_model=BookingRead)
def confirm_payment(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = booking_read(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return confirm_booking_payment(db, booking_id)

@router.get("/user/me", response_model=List[BookingWithDetails])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_bookings_by_user(db, user_id=current_user.id)

@router.get("/all", response_model=List[BookingWithDetails])
def list_all_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")
    return get_all_bookings(db)

@router.get("/{booking_id}", response_model=BookingWithDetails)
def get_booking_details(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = booking_read(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.id and current_user.role != "ADMIN":
         raise HTTPException(status_code=403, detail="Not authorized") 
    return booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking_endpoint(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = booking_read(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Only admin can delete bookings
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can delete bookings")
    
    success = delete_booking(db, booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return None
