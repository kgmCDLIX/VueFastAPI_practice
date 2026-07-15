from fastapi import APIRouter

from ..schemas.token import Token
from ..schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate):
    return {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "role": "geolog",
        "is_active": True,
    }

@router.post("/login", response_model=Token)
def login():
    return {
        "access_token": "temporary_test_token",
        "token_type": "bearer",
    }