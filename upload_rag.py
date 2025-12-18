import time
import sqlite3
from google import genai
from google.genai import types

# --- SETTINGS ---
FILE_TO_UPLOAD = 'security_docs.txt'
STORE_DISPLAY_NAME = 'SecureAssist_KB_2025'
DB_NAME = "secureassist.db"

client = genai.Client()

def setup_local_db():
    print("Initializing local database...")
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS InteractionLog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_query TEXT,
            ai_response TEXT,
            store_name TEXT
        )
    """)
    conn.close()
    print("✅ Local DB Ready.")

def upload_to_gemini():
    print("Creating Cloud Knowledge Base...")
    store = client.file_search_stores.create(config={'display_name': STORE_DISPLAY_NAME})
    
    operation = client.file_search_stores.upload_to_file_search_store(
        file=FILE_TO_UPLOAD,
        file_search_store_name=store.name,
        config={ 'display_name': FILE_TO_UPLOAD }
    )
    
    while not operation.done:
        print("⏳ Syncing files...")
        time.sleep(5)
        operation = client.operations.get(operation)
    
    print(f"\n✅ Cloud Sync Complete!")
    print(f"Update your app.py with: FILE_SEARCH_STORE_NAME = '{store.name}'")

if __name__ == '__main__':
    setup_local_db()
    upload_to_gemini()
