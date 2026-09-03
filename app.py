"""
Adi — Your Personal Schedule & Reminder Website
------------------------------------------------
Run locally with:  python app.py
Then open:          http://127.0.0.1:5000
"""

import sqlite3
import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "adi-secret-key-change-this-later"

DB_PATH = os.path.join(os.path.dirname(__file__), "adi.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        event_date TEXT NOT NULL,
        event_time TEXT,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)
    conn.commit()
    conn.close()


def current_user_id():
    return session.get("user_id")


def login_required(view_func):
    def wrapper(*args, **kwargs):
        if not current_user_id():
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            flash("Please fill in both fields.")
            return redirect(url_for("register"))

        conn = get_db()
        existing = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            conn.close()
            flash("That username is already taken.")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        conn.close()

        flash("Account created! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def home():
    if current_user_id():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM events WHERE user_id = ? ORDER BY event_date, event_time",
        (current_user_id(),)
    ).fetchall()
    conn.close()

    events = [dict(row) for row in rows]
    today_str = date.today().isoformat()

    return render_template("dashboard.html", events=events, today=today_str, username=session.get("username"))


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":
        title = request.form["title"].strip()
        event_date = request.form["event_date"]
        event_time = request.form.get("event_time", "")
        notes = request.form.get("notes", "")

        if not title or not event_date:
            flash("Title and date are required.")
            return redirect(url_for("add_event"))

        conn = get_db()
        conn.execute(
            "INSERT INTO events (user_id, title, event_date, event_time, notes) VALUES (?, ?, ?, ?, ?)",
            (current_user_id(), title, event_date, event_time, notes)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add_event.html")


@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    conn = get_db()
    event = conn.execute(
        "SELECT * FROM events WHERE id = ? AND user_id = ?", (event_id, current_user_id())
    ).fetchone()

    if event is None:
        conn.close()
        flash("Event not found.")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form["title"].strip()
        event_date = request.form["event_date"]
        event_time = request.form.get("event_time", "")
        notes = request.form.get("notes", "")

        conn.execute(
            "UPDATE events SET title=?, event_date=?, event_time=?, notes=? WHERE id=? AND user_id=?",
            (title, event_date, event_time, notes, event_id, current_user_id())
        )
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("edit_event.html", event=event)


@app.route("/delete/<int:event_id>")
@login_required
def delete_event(event_id):
    conn = get_db()
    conn.execute("DELETE FROM events WHERE id = ? AND user_id = ?", (event_id, current_user_id()))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
