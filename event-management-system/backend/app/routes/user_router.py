from fastapi import APIRouter, Depends, FastAPI, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserCreateResponse, UserUpdate
from app.core.database import get_db
from app.crud.user_crud import create_user, get_user_by_email, update_user
from app.core.security import get_password_hash
import shutil
from pathlib import Path
import uuid

router = APIRouter(prefix="/users", tags=["Users"])

from app.models.user import User
from app.routes.wishlist import get_current_user

# Ensure upload directory exists
PROFILE_IMG_DIR = Path("uploads/profile_images")
PROFILE_IMG_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/", response_model=UserCreateResponse)
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password before storing
    user_data = user.dict()
    user_data['password'] = get_password_hash(user.password)
    user_create = UserCreate(**user_data)
    
    return create_user(db, user_create)

@router.put("/me")
def update_my_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Filter out None values
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    
    # Prevent changing role via this endpoint for safety (though schema allows it)
    if 'role' in update_data:
        del update_data['role']
        
    return update_user(db, current_user.id, update_data)

@router.post("/me/image")
async def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Generate unique filename
        file_ext = file.filename.split(".")[-1]
        filename = f"user_{current_user.id}_{uuid.uuid4().hex[:8]}.{file_ext}"
        file_path = PROFILE_IMG_DIR / filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Update user profile
        image_url = f"/uploads/profile_images/{filename}"
        update_user(db, current_user.id, {"profile_image": image_url})
        
        return {"profile_image": image_url}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload image: {str(e)}")

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return {"message": f"Details of User {user_id}"}

