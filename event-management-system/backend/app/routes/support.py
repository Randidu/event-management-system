from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ticket_schema import TicketCreate, TicketRead, TicketCommentCreate, TicketCommentRead
from app.crud.ticket_crud import create_ticket, get_ticket, get_tickets_by_user, create_comment
from app.routes.wishlist import get_current_user 
from app.models.user import User

router = APIRouter(prefix="/support", tags=["Support"])

from app.schemas.ticket_schema import TicketCreate, TicketRead, TicketCommentCreate, TicketCommentRead, TicketBase

@router.post("/tickets", response_model=TicketRead)
def create_new_ticket(ticket: TicketBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_ticket(db, ticket, requester_id=current_user.id)

@router.get("/tickets", response_model=list[TicketRead])
def get_my_tickets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_tickets_by_user(db, user_id=current_user.id)

@router.get("/tickets/{ticket_id}", response_model=TicketRead)
def get_ticket_detail(ticket_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.requester_id != current_user.id and current_user.role != "ADMIN": # Assuming role check
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")
    return ticket

@router.post("/tickets/{ticket_id}/comments", response_model=TicketCommentRead)
def add_comment(ticket_id: int, comment: TicketCommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
         raise HTTPException(status_code=404, detail="Ticket not found")
    # Allow requester or admin to comment
    if ticket.requester_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized to comment on this ticket")
        
    return create_comment(db, comment, ticket_id, author_id=current_user.id)
