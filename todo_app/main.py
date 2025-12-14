from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3
import os

app = FastAPI(title="TODO Service")

DB_PATH = "/app/data/todo.db"
SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


class TodoItem(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


def read_sql(filename: str) -> str:
    with open(os.path.join(SQL_DIR, filename), 'r') as f:
        return f.read()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(read_sql("init.sql"))
    conn.commit()
    conn.close()


init_db()


@app.post("/items")
def create_item(item: TodoItem):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        read_sql("create_item.sql"),
        (item.title, item.description, item.completed)
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return {"id": item_id, **item.dict()}


@app.get("/items")
def get_items():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(read_sql("get_all_items.sql"))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/items/{item_id}")
def get_item(item_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(read_sql("get_item_by_id.sql"), (item_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(row)


@app.put("/items/{item_id}")
def update_item(item_id: int, item: TodoItemUpdate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(read_sql("get_item_by_id.sql"), (item_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")

    updates = []
    values = []
    if item.title is not None:
        updates.append("title = ?")
        values.append(item.title)
    if item.description is not None:
        updates.append("description = ?")
        values.append(item.description)
    if item.completed is not None:
        updates.append("completed = ?")
        values.append(item.completed)

    if updates:
        values.append(item_id)
        query = read_sql("update_item.sql").replace("{updates}", ", ".join(updates))
        cursor.execute(query, values)
        conn.commit()

    conn.close()
    return {"message": "Item updated", "id": item_id}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(read_sql("delete_item.sql"), (item_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")
    conn.commit()
    conn.close()
    return {"message": "Item deleted", "id": item_id}