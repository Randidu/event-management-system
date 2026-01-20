from sqlalchemy.orm import Session
from app.models.wishlist import WishlistItem
from app.schemas.wishlist_schema import WishlistItemCreate

def get_wishlist(db: Session, user_id: int):
    return db.query(WishlistItem).filter(WishlistItem.user_id == user_id).all()

def add_to_wishlist(db: Session, wishlist_item: WishlistItemCreate):
    db_item = WishlistItem(user_id=wishlist_item.user_id, event_id=wishlist_item.event_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_from_wishlist(db: Session, user_id: int, event_id: int):
    item = db.query(WishlistItem).filter(WishlistItem.user_id == user_id, WishlistItem.event_id == event_id).first()
    if item:
        db.delete(item)
        db.commit()
        return True
    return False

def get_wishlist_item(db: Session, user_id: int, event_id: int):
    return db.query(WishlistItem).filter(WishlistItem.user_id == user_id, WishlistItem.event_id == event_id).first()
