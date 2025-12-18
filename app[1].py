import os
import sqlite3
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from google import genai
from google.genai import types

# --- CONFIGURATION ---
# Keeping your exact store name as requested
FILE_SEARCH_STORE_NAME = 'fileSearchStores/secureassistkb2025-wduwpz6329cy'
DB_NAME = "secureassist.db"

app = Flask(__name__)
app.secret_key = "SECURE_ASSIST_SUPER_SECRET_KEY_2025"

# Admin Credentials
ADMIN_USER = "admin"
ADMIN_PASS = "password123"

MODELS_TO_TRY = ["gemini-3-flash-preview", "gemini-2.5-flash-lite", "gemini-2.0-flash"]

# --- API CLIENT SETUP ---
client = None
try:
    client = genai.Client()
except Exception as e:
    print(f"Gemini Client failed: {e}")

RAG_CONFIG_BASE = {
    "system_instruction": "You are SecureAssist. 1. If info is from knowledge base, start with [INTERNAL]. 2. If general, start with [GLOBAL]. 3. Hotline: 1-800-888-DANGER.",
    "tools": [types.Tool(file_search=types.FileSearch(file_search_store_names=[FILE_SEARCH_STORE_NAME]))]
}

# --- DATABASE HELPERS ---
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# 🛠️ MODERN FIX: Initializing DB outside of the request cycle
with app.app_context():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS InteractionLog (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
            user_query TEXT, 
            ai_response TEXT, 
            store_name TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- ROUTES ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "")
    
    if not query:
        return jsonify({"response": "Please enter a question."})

    ai_response = "Error: Could not reach AI models."
    used_model = "None"

    # Fallback Loop
    for model_id in MODELS_TO_TRY:
        try:
            response = client.models.generate_content(
                model=model_id, 
                contents=[query], 
                config=types.GenerateContentConfig(**RAG_CONFIG_BASE)
            )
            ai_response = response.text
            used_model = model_id
            break
        except Exception as e:
            print(f"Model {model_id} failed: {e}")
            continue

    # Log to Database
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO InteractionLog (user_query, ai_response, store_name) VALUES (?, ?, ?)", 
                     (query, ai_response, used_model))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Log Error: {e}")

    return jsonify({"response": ai_response, "model": used_model})

# --- ADMIN ROUTES ---
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user_input = request.form.get('user')
        pass_input = request.form.get('pass')
        if user_input == ADMIN_USER and pass_input == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid Credentials. Access Denied."
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get('admin'): 
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM InteractionLog ORDER BY timestamp DESC").fetchall()
    conn.close()
    return render_template("admin_dashboard.html", logs=logs)

@app.route("/admin/delete/<int:id>")
def delete_log(id):
    if not session.get('admin'): 
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    conn.execute("DELETE FROM InteractionLog WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route("/admin/logout")
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == "__main__":
    app.run(debug=True)