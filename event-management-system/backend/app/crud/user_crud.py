from sqlalchemy.orm import Session
from ..models.user import User  
from ..schemas.user_schema import UserCreate


def create_user(db: Session, user_create: UserCreate) -> User:
    new_user = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        email=user_create.email,
        phone_number=user_create.phone_number,
        role=user_create.role,
        profile_image=user_create.profile_image,
        hashed_password=user_create.password  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_id: int, update_data: dict) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return "Deleted Successfully"

def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()