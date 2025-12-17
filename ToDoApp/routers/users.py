# ============================================================
#                           IMPORTS
# ============================================================
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users, ToDos
from .auth import get_current_user, bcrypt_context


# ============================================================
#                     ROUTER CONFIGURATION
# ============================================================
router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# ============================================================
#                    DATABASE DEPENDENCY
# ============================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# ============================================================
#                     PYDANTIC SCHEMAS
# ============================================================
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


# ============================================================
#                       USER ROUTES
# ============================================================

# ----------------------------
# Get current user
# ----------------------------
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(
    user: user_dependency,
    db: db_dependency
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return (
        db.query(Users)
        .filter(user.get("id") == Users.id)
        .first()
    )


# ----------------------------
# Change user password
# ----------------------------
@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    user_verification: UserVerification
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    user_model = (
        db.query(Users)
        .filter(user.get("id") == Users.id)
        .first()
    )

    if not bcrypt_context.verify(
        user_verification.password,
        user_model.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error on password change"
        )

    user_model.hashed_password = bcrypt_context.hash(
        user_verification.new_password
    )

    db.add(user_model)
    db.commit()


# ----------------------------
# Change user phone number
# ----------------------------
@router.put(
    "/phonenumber/{phone_number}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def change_phone_number(
    user: user_dependency,
    db: db_dependency,
    phone_number: str
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization failed"
        )

    user_model = (
        db.query(Users)
        .filter(user.get("id") == Users.id)
        .first()
    )

    user_model.phone_number = phone_number

    db.add(user_model)
    db.commit()
