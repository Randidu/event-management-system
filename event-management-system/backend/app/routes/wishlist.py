from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.wishlist import WishlistItem
from app.schemas.wishlist_schema import WishlistItemCreate, WishlistItemRead
from app.crud.wishlist_crud import get_wishlist, add_to_wishlist, remove_from_wishlist, get_wishlist_item
from app.core.security import oauth2_scheme, verify_jwt_token
from app.crud.user_crud import get_user_by_email

# NOTE: ideally we should move get_current_user to a dependency in core/deps.py or similar to avoid repeating logic
# For now, I will implement a local get_current_user dependency or re-use if existing.
# security.py has verify_jwt_token but no direct get_current_user dependency that extracts user.

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_jwt_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/", response_model=list[dict])
def read_wishlist(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        from app.models.event import Event
        
        # Query wishlist items with related event details
        items = db.query(WishlistItem, Event).join(
            Event, WishlistItem.event_id == Event.id
        ).filter(
            WishlistItem.user_id == current_user.id
        ).all()
        
        result = []
        for wishlist_item, event in items:
            result.append({
                "id": wishlist_item.id,
                "event_id": wishlist_item.event_id,
                "added_at": wishlist_item.added_at.isoformat() if wishlist_item.added_at else None,
                "user_id": wishlist_item.user_id,
                "event": {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "category": event.category,
                    "location": event.location,
                    "starts_at": event.starts_at.isoformat() if event.starts_at else None,
                    "ends_at": event.ends_at.isoformat() if event.ends_at else None,
                    "poster_url": event.poster_url,
                    "ga_ticket_price": float(event.ga_ticket_price) if event.ga_ticket_price else 0,
                    "vip_ticket_price": float(event.vip_ticket_price) if event.vip_ticket_price else 0,
                    "pa_ticket_price": float(event.pa_ticket_price) if event.pa_ticket_price else 0,
                }
            })
        
        return result
    except Exception as e:
        print(f"Wishlist error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error loading wishlist: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error loading wishlist: {str(e)}")

@router.post("/", response_model=dict)
def create_wishlist_item(event_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    from pydantic import BaseModel
    
    existing = get_wishlist_item(db, user_id=current_user.id, event_id=event_id)
    if existing:
        raise HTTPException(status_code=400, detail="Item already in wishlist")
    
    # Create item with current user
    item = WishlistItemCreate(user_id=current_user.id, event_id=event_id)
    new_item = add_to_wishlist(db, item)
    
    # Return dict response
    return {
        "id": new_item.id,
        "user_id": new_item.user_id,
        "event_id": new_item.event_id,
        "added_at": new_item.added_at.isoformat() if new_item.added_at else None
    }

@router.delete("/{event_id}")
def delete_wishlist_item(event_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    success = remove_from_wishlist(db, user_id=current_user.id, event_id=event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found in wishlist")
    return {"message": "Item removed from wishlist"}
