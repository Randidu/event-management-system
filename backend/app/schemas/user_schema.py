from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole = UserRole.CUSTOMER
    profile_image: str | None = None

class UserCreate(UserBase):
    password: str

class UserCreateResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: UserRole
    profile_image: str | None = None

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    profile_image: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None

class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
