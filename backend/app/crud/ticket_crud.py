from sqlalchemy.orm import Session
from app.models.ticket import Ticket, TicketComment, TicketStatus
from app.schemas.ticket_schema import TicketCreate, TicketCommentCreate

def create_ticket(db: Session, ticket: TicketCreate, requester_id: int):
    db_ticket = Ticket(
        subject=ticket.subject,
        description=ticket.description,
        requester_id=requester_id,
        status=TicketStatus.OPEN
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: int):
    from sqlalchemy.orm import joinedload
    return db.query(Ticket).options(joinedload(Ticket.comments).joinedload(TicketComment.author)).filter(Ticket.id == ticket_id).first()

def get_tickets_by_user(db: Session, user_id: int):
    from sqlalchemy.orm import joinedload
    return db.query(Ticket).options(joinedload(Ticket.comments).joinedload(TicketComment.author)).filter(Ticket.requester_id == user_id).all()

def get_all_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ticket).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: TicketCommentCreate, ticket_id: int, author_id: int):
    db_comment = TicketComment(
        ticket_id=ticket_id,
        author_id=author_id,
        body=comment.body
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_ticket_status(db: Session, ticket_id: int, status: TicketStatus):
    ticket = get_ticket(db, ticket_id)
    if ticket:
        ticket.status = status
        db.commit()
        db.refresh(ticket)
    return ticket

def assign_ticket(db: Session, ticket_id: int, assignee_id: int):
    ticket = get_ticket(db, ticket_id)
    if ticket:
        ticket.assignee_id = assignee_id
        db.commit()
        db.refresh(ticket)
    return ticket