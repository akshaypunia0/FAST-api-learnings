from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

# Engine create (DB connection)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session (DB operations k liye)
sessionlocal = sessionmaker(bind=engine)

# Base (Models create krne k liye)
Base = declarative_base()

# Table (Model)

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

# Create Todo
@app.post("/todos")
def create_todo(title: str, db: Session = Depends(get_db)):
    todo = Todo(title= title, completed= "False")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        "message": "Todo created successfully",
        "todo": todo
    }

# Fetch all todo data from db
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return {
        "Total": len(todos),
        "message": 'todos fetched successfully',
        "todos": todos
    }

# Fetch single todo data from db by id
@app.get("/todo/{id}")
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )
    
    return {
        "message": 'todos fetched successfully',
        "todos": todo
    }

# Update todo
@app.put("/todo/{id}")
def update_todo(id: int, title: str, completed = "False", db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    todo.title = title
    todo.completed = completed

    db.commit()
    db.refresh(todo)

    return {
        "messge": "Todo updated",
        "todo": todo
    }

# Delete todo
@app.delete("/todo/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )
    
    db.delete(todo)
    db.commit()
    
    return {
        "message": "Todo deleted",
        "todo": todo
    }