from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import sqlite3
import random
import string

# FastAPI app initialize karna
app = FastAPI(title="URL Shortener API")

# Database setup function
def init_db():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    # Table banayenge jisme id, original_url aur short_code save hoga
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS url_mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

# App start hote hi database initialize ho jayega
init_db()

# User se input lene ke liye format
class URLRequest(BaseModel):
    url: str

# 6 character ka random short code generate karne ka function
def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# 1. POST Endpoint: Long URL ko short karne ke liye
@app.post("/shorten")
def shorten_url(request: URLRequest):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    
    short_code = generate_short_code()
    
    try:
        # Database mein original URL aur naya short code save karna
        cursor.execute("INSERT INTO url_mapping (original_url, short_code) VALUES (?, ?)", 
                       (request.url, short_code))
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail="Database error")
    
    conn.close()
    
    # Return response jisme short URL hoga
    return {"original_url": request.url, "short_url": f"http://127.0.0.1:8000/{short_code}"}

# 2. GET Endpoint: Short URL ko open karke original URL par redirect karne ke liye
@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    
    # Database mein check karna ki short_code exist karta hai ya nahi
    cursor.execute("SELECT original_url FROM url_mapping WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        # Agar code mila, toh original website par bhej do
        return RedirectResponse(url=result[0])
    else:
        # Agar code nahi mila, toh 404 error dikhao
        raise HTTPException(status_code=404, detail="URL not found")
