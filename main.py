from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

todo_db: List[TodoItem] = []

# Create
@app.post("/todos/", response_model=TodoItem)
def create_todo(todo: TodoItem):
    for item in todo_db:
        if item.id == todo.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists.")
    
    todo_db.append(todo)
    return todo

# Read All Todos
@app.get("/todos/", response_model=List[TodoItem])
def read_todos():
    return todo_db

# Read One Todo
@app.get("/todos/{todo_id}", response_model=TodoItem)
def read_todo(todo_id: int):
    for todo in todo_db:
        if todo.id == todo_id:
            return todo
    
    raise HTTPException(status_code=404, detail="Todo not found")

# Update
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    for index, todo in enumerate(todo_db):
        if todo.id == todo_id:
            todo_db[index] = updated_todo
            return updated_todo
    
    raise HTTPException(status_code=404, detail="Todo not found")

# Delete
@app.delete("/todos/{todo_id}", response_model=TodoItem)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todo_db):
        if todo.id == todo_id:
            deleted_todo = todo_db.pop(index)
            return deleted_todo
        
    raise HTTPException(status_code=404, detail="Todo not found")