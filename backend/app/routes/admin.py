from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.schemas.user_schema import UserRead
from app.schemas.ticket_schema import TicketRead, TicketUpdate, TicketStatus
from app.crud.user_crud import list_users, delete_user
from app.crud.ticket_crud import get_all_tickets, update_ticket_status, assign_ticket, get_ticket
from app.routes.wishlist import get_current_user
from app.models.user import User, UserRole

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

@router.get("/users", response_model=list[UserRead])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return list_users(db, skip=skip, limit=limit)

@router.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return delete_user(db, user_id)

@router.get("/tickets", response_model=list[TicketRead])
def read_all_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return get_all_tickets(db, skip=skip, limit=limit)

@router.put("/tickets/{ticket_id}/status", response_model=TicketRead)
def change_ticket_status(ticket_id: int, status: TicketStatus, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    ticket = update_ticket_status(db, ticket_id, status)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("/tickets/{ticket_id}/assign/{assignee_id}", response_model=TicketRead)
def assign_ticket_to_user(ticket_id: int, assignee_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    ticket = assign_ticket(db, ticket_id, assignee_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/dashboard-stats")
def get_dashboard_stats(days: int = 30, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    from app.models.booking import Booking
    from app.models.event import Event
    from app.models.ticket import Ticket # Support tickets
    from sqlalchemy import func, desc
    from datetime import datetime, timedelta

    # Calculate date cutoff
    if days >= 9999:
        date_cutoff = None
    else:
        date_cutoff = datetime.now() - timedelta(days=days)

    # 1. Total Revenue (sum of completed bookings within date range)
    revenue_query = db.query(func.sum(Booking.total_price)).filter(
        Booking.payment_status == "PAID"
    )
    if date_cutoff:
        revenue_query = revenue_query.filter(Booking.booked_at >= date_cutoff)
    total_revenue = revenue_query.scalar() or 0.0

    # 2. Active Users (total user count)
    active_users = db.query(func.count(User.id)).scalar() or 0

    # 3. Open Support Tickets
    open_tickets = db.query(func.count(Ticket.id)).filter(
        Ticket.status == "OPEN"
    ).scalar() or 0

    # 4. Upcoming Events Count
    upcoming_events_count = db.query(func.count(Event.id)).filter(
        Event.starts_at > datetime.now()
    ).scalar() or 0

    # 5. Recent Signups (last 5)
    recent_signups = db.query(User).order_by(desc(User.created_at)).limit(5).all()

    # 6. Upcoming Events List (next 3)
    upcoming_events = db.query(Event).filter(
        Event.starts_at > datetime.now()
    ).order_by(Event.starts_at).limit(3).all()

    return {
        "total_revenue": total_revenue,
        "active_users": active_users,
        "open_tickets": open_tickets,
        "upcoming_events_count": upcoming_events_count,
        "recent_signups": recent_signups,
        "upcoming_events": upcoming_events
    }

from app.schemas.user_schema import UserCreate, UserCreateResponse, UserUpdate
from app.crud.user_crud import create_user, update_user as crud_update_user
from app.core.security import get_password_hash

@router.post("/users", response_model=UserCreateResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    # Check if user exists (handled in crud/router usually, but good to check)
    from app.crud.user_crud import get_user_by_email
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = user.dict()
    user_data['password'] = get_password_hash(user.password)
    user_create = UserCreate(**user_data)
    return create_user(db, user_create)

@router.patch("/users/{user_id}", response_model=UserRead)
def update_user_details(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    # Update user (specifically role or active status)
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    return crud_update_user(db, user_id, update_data)

@router.get("/users/{user_id}", response_model=UserRead)
def get_user_details(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    from app.crud.user_crud import get_user_by_id
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/reports")
def get_reports(
    days: int = 30,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    from app.models.booking import Booking
    from app.models.event import Event
    from app.models.user import User as DBUser
    from app.models.ticket import Ticket # Support tickets
    from sqlalchemy import func, desc, and_
    from datetime import datetime, timedelta

    try:
        start_date = datetime.now() - timedelta(days=days)

        # 1. Stats in Period
        revenue = db.query(func.sum(Booking.total_price)).filter(
            and_(Booking.payment_status == "PAID", Booking.booked_at >= start_date)
        ).scalar() or 0.0

        tickets_sold = db.query(func.count(Booking.id)).filter(
            and_(Booking.payment_status == "PAID", Booking.booked_at >= start_date)
        ).scalar() or 0

        new_users = db.query(func.count(DBUser.id)).filter(
            DBUser.created_at >= start_date
        ).scalar() or 0

        # Total open tickets (not just in period)
        open_support = db.query(func.count(Ticket.id)).filter(Ticket.status == "OPEN").scalar() or 0

        # 2. Top Events (by ticket sales in period)
        # Group bookings by event_id, count them
        top_events = db.query(
            Event.title,
            func.count(Booking.id).label('sales_count')
        ).join(Booking).filter(
            and_(Booking.payment_status == "PAID", Booking.booked_at >= start_date)
        ).group_by(Event.id).order_by(desc('sales_count')).limit(5).all()
        
        # Format for chart (Title, Count, Percentage relative to max)
        max_sales = top_events[0].sales_count if top_events else 1
        chart_data = [
            {"label": e.title, "value": e.sales_count, "percent": int((e.sales_count / max_sales) * 100)} 
            for e in top_events
        ]

        # 3. Recent Transactions (Completed Bookings)
        transactions = db.query(Booking).options(
            joinedload(Booking.user),
            joinedload(Booking.event)
        ).filter(
            Booking.payment_status == "PAID"
        ).order_by(desc(Booking.booked_at)).limit(10).all()

        # Manual serialization for transactions to avoid circular refs/heavy schemas
        tx_list = [
            {
                "id": str(b.id), # Booking ID usually int, but reports show hash? using ID for now
                "user_name": f"{b.user.first_name} {b.user.last_name}",
                "event_title": b.event.title,
                "date": b.booked_at,
                "amount": b.total_price,
                "status": b.payment_status
            } for b in transactions
        ]

        return {
            "period_days": days,
            "revenue": revenue,
            "tickets_sold": tickets_sold,
            "new_users": new_users,
            "open_support": open_support,
            "chart_data": chart_data,
            "transactions": tx_list
        }
    except Exception as e:
        print(f"Error in get_reports: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/events/sales")
def get_event_sales_stats(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    """Get ticket sales statistics for all events"""
    from app.models.booking import Booking
    from app.models.event import Event
    from sqlalchemy import func
    
    # Get all events with their ticket sales count and revenue
    sales_stats = db.query(
        Event.id,
        Event.title,
        Event.capacity,
        Event.starts_at,
        Event.status,
        func.coalesce(func.sum(Booking.quantity), 0).label('tickets_sold'),
        func.coalesce(func.sum(Booking.total_price), 0).label('revenue')
    ).outerjoin(
        Booking, 
        (Booking.event_id == Event.id) & (Booking.payment_status == "PAID")
    ).group_by(Event.id).all()
    
    result = []
    for stat in sales_stats:
        tickets_sold = int(stat.tickets_sold) if stat.tickets_sold else 0
        capacity = stat.capacity or 0
        available = max(0, capacity - tickets_sold)
        sold_percentage = round((tickets_sold / capacity * 100), 1) if capacity > 0 else 0
        
        result.append({
            "event_id": stat.id,
            "title": stat.title,
            "capacity": capacity,
            "tickets_sold": tickets_sold,
            "tickets_available": available,
            "sold_percentage": sold_percentage,
            "revenue": float(stat.revenue) if stat.revenue else 0,
            "starts_at": stat.starts_at,
            "status": stat.status
        })
    
    return result

@router.get("/events/{event_id}/sales")
def get_single_event_sales(event_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    """Get detailed ticket sales for a specific event"""
    from app.models.booking import Booking
    from app.models.event import Event
    from sqlalchemy import func
    
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get bookings for this event
    bookings = db.query(Booking).options(
        joinedload(Booking.user)
    ).filter(Booking.event_id == event_id).all()
    
    # Calculate stats
    confirmed_bookings = [b for b in bookings if b.payment_status == "PAID"]
    pending_bookings = [b for b in bookings if b.payment_status == "PENDING"]
    cancelled_bookings = [b for b in bookings if b.status == "CANCELLED"]
    
    total_sold = sum(b.quantity for b in confirmed_bookings)
    total_revenue = sum(b.total_price for b in confirmed_bookings)
    pending_count = sum(b.quantity for b in pending_bookings)
    
    return {
        "event": {
            "id": event.id,
            "title": event.title,
            "capacity": event.capacity,
            "starts_at": event.starts_at,
            "status": event.status,
            "ga_ticket_price": event.ga_ticket_price,
            "vip_ticket_price": event.vip_ticket_price
        },
        "stats": {
            "tickets_sold": total_sold,
            "tickets_available": max(0, (event.capacity or 0) - total_sold),
            "sold_percentage": round((total_sold / event.capacity * 100), 1) if event.capacity else 0,
            "total_revenue": total_revenue,
            "pending_tickets": pending_count,
            "total_bookings": len(bookings),
            "confirmed_bookings": len(confirmed_bookings),
            "cancelled_bookings": len(cancelled_bookings)
        },
        "bookings": [
            {
                "id": b.id,
                "user_name": f"{b.user.first_name} {b.user.last_name}" if b.user else "N/A",
                "user_email": b.user.email if b.user else "N/A",
                "quantity": b.quantity,
                "total_price": b.total_price,
                "status": b.status,
                "payment_status": b.payment_status,
                "booked_at": b.booked_at
            } for b in bookings
        ]
    }

