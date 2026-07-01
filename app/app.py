from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import redis
import os
import time

app = Flask(__name__)

def get_db():
    retries = 5
    while retries > 0:
        try:
            return psycopg2.connect(
                host=os.environ.get("DB_HOST", "postgres"),
                database=os.environ.get("DB_NAME", "cybernotesdb"),
                user=os.environ.get("DB_USER", "cyberuser"),
                password=os.environ.get("DB_PASSWORD", "cyberpass")
            )
        except Exception:
            retries -= 1
            time.sleep(2)
    raise Exception("Could not connect to database")

def get_redis():
    return redis.Redis(
        host=os.environ.get("REDIS_HOST", "redis"),
        decode_responses=True
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            category VARCHAR(100) DEFAULT 'General',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    try:
        r = get_redis()
        visits = r.incr("visit_count")
    except:
        visits = 0
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, title, content, category, created_at FROM notes ORDER BY created_at DESC")
        notes = cur.fetchall()
        cur.close()
        conn.close()
    except:
        notes = []
    return render_template("index.html", notes=notes, visits=visits)

@app.route("/add", methods=["GET", "POST"])
def add_note():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (title, content, category) VALUES (%s, %s, %s)", (title, content, category))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add_note.html")

@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
