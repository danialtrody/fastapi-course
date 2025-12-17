# ============================================================
#                           IMPORTS
# ============================================================
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import ToDos
from .auth import get_current_user


# ============================================================
#                     ROUTER CONFIGURATION
# ============================================================
router = APIRouter()


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
#                     PYDANTIC REQUEST MODEL
# ============================================================
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new Todo",
                "author": "danial",
                "description": "A new description of a todo",
                "priority": 5,
                "complete": "false"
            }
        }
    }


# ============================================================
#                       TODO ROUTES
# ============================================================

# ----------------------------
# Get all todos for user
# ----------------------------
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(
    user: user_dependency,
    db: db_dependency
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Failed"
        )

    return (
        db.query(ToDos)
        .filter(ToDos.owner_id == user.get("id"))
        .all()
    )


# ----------------------------
# Get single todo
# ----------------------------
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Failed"
        )

    todo_model = (
        db.query(ToDos)
        .filter(ToDos.id == todo_id)
        .filter(ToDos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ToDo not found"
        )

    return todo_model


# ----------------------------
# Create todo
# ----------------------------
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Failed"
        )

    todo_model = ToDos(
        **todo_request.dict(),
        owner_id=user.get("id")
    )

    db.add(todo_model)
    db.commit()


# ----------------------------
# Update todo
# ----------------------------
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Failed"
        )

    todo_model = (
        db.query(ToDos)
        .filter(ToDos.id == todo_id)
        .filter(ToDos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ToDo not found"
        )

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


# ----------------------------
# Delete todo
# ----------------------------
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Failed"
        )

    todo_model = (
        db.query(ToDos)
        .filter(ToDos.id == todo_id)
        .filter(ToDos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ToDo not found"
        )

    (
        db.query(ToDos)
        .filter(ToDos.id == todo_id)
        .filter(ToDos.owner_id == user.get("id"))
        .delete()
    )

    db.commit()
