import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establishes a connection to the AlloyDB/PostgreSQL instance."""
    # Fallback to a local test DB if the env var isn't set yet
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/postgres")
    try:
        conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_dummy_data():
    """Creates the table and inserts dummy notes for the hackathon demo."""
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meeting_notes (
            id SERIAL PRIMARY KEY,
            topic VARCHAR(255),
            date DATE,
            notes TEXT
        );
    """)
    
    # Clear existing to avoid duplicates during testing
    cursor.execute("TRUNCATE TABLE meeting_notes RESTART IDENTITY;")
    
    # Insert Track 3 demo data
    dummy_data = [
        ("engineering sync", "2026-04-01", "Discussed Q2 roadmap. Need to refactor the Auth module. Blockers: API rate limits."),
        ("engineering sync", "2026-03-25", "Reviewed pull requests. Decided to migrate to AlloyDB for better vector search capabilities."),
        ("marketing sync", "2026-04-02", "Finalized the launch copy for the new feature.")
    ]
    
    cursor.executemany(
        "INSERT INTO meeting_notes (topic, date, notes) VALUES (%s, %s, %s)",
        dummy_data
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Dummy data initialized in database.")

def query_meeting_notes(topic: str) -> str:
    """Tool: Queries the database for past meeting notes on a specific topic."""
    conn = get_db_connection()
    if not conn:
        return "Error: Could not connect to database."
    
    cursor = conn.cursor()
    cursor.execute("SELECT date, notes FROM meeting_notes WHERE topic = %s ORDER BY date DESC", (topic.lower(),))
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not rows:
        return f"No notes found for topic: {topic}"
    
    result = f"--- Past Notes for {topic} ---\n"
    for row in rows:
        result += f"Date: {row['date']} | Notes: {row['notes']}\n"
    return result