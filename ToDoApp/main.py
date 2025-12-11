# ============================================================
#                        IMPORTS
# ============================================================
from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status

import models
from models import ToDos
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session


# ============================================================
#                 APP & DATABASE INITIALIZATION
# ============================================================
app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# ============================================================
#                     DATABASE DEPENDENCY
# ============================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# ============================================================
#                     PYDANTIC REQUEST MODEL
# ============================================================
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# ============================================================
#                        GET ALL TODOS
# ============================================================
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(ToDos).all()


# ============================================================
#                        GET ONE TODO
# ============================================================
@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="ToDo not found")

    return todo_model


# ============================================================
#                        CREATE TODO
# ============================================================
@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = ToDos(**todo_request.dict())
    db.add(todo_model)
    db.commit()


# ============================================================
#                        UPDATE TODO
# ============================================================
@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):

    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="ToDo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


# ============================================================
#                        DELETE TODO
# ============================================================
@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="ToDo not found")

    db.query(ToDos).filter(ToDos.id == todo_id).delete()
    db.commit()
