from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import sqlite3
import os
import hashlib

app = FastAPI(title="URL Shortener Service")

DB_PATH = "/app/data/urls.db"
SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


class URLCreate(BaseModel):
    url: HttpUrl


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


def generate_short_id(url: str) -> str:
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:8]


@app.post("/shorten")
def shorten_url(data: URLCreate):
    url = str(data.url)
    short_id = generate_short_id(url)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(read_sql("check_existing.sql"), (short_id,))
    existing = cursor.fetchone()

    if not existing:
        cursor.execute(read_sql("insert_url.sql"), (short_id, url))
        conn.commit()

    conn.close()
    return {"short_id": short_id, "short_url": f"/{short_id}", "original_url": url}


@app.get("/{short_id}")
def redirect_to_url(short_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(read_sql("get_url_by_id.sql"), (short_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=row[1])


@app.get("/stats/{short_id}")
def get_stats(short_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(read_sql("get_url_by_id.sql"), (short_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return dict(row)