import sqlite3
from datetime import datetime

DB_PATH = "supportdesk.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id   TEXT UNIQUE NOT NULL,
            customer_name  TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            subject     TEXT NOT NULL,
            description TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'Open',
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id  TEXT NOT NULL,
            note_text  TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
        )
    """)
    conn.commit()
    conn.close()

def next_ticket_id():
    conn = get_conn()
    row = conn.execute("SELECT COUNT(*) as cnt FROM tickets").fetchone()
    n = row["cnt"] + 1
    conn.close()
    return f"TKT-{str(n).zfill(3)}"

def create_ticket(name, email, subject, description):
    conn = get_conn()
    ticket_id = next_ticket_id()
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO tickets (ticket_id, customer_name, customer_email, subject, description, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'Open', ?, ?)
    """, (ticket_id, name, email, subject, description, now, now))
    conn.commit()
    row = conn.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
    conn.close()
    return dict(row)

def get_tickets(status=None, search=None):
    conn = get_conn()
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []
    if status:
        query += " AND status=?"
        params.append(status)
    if search:
        q = f"%{search}%"
        query += " AND (customer_name LIKE ? OR customer_email LIKE ? OR ticket_id LIKE ? OR subject LIKE ? OR description LIKE ?)"
        params.extend([q, q, q, q, q])
    query += " ORDER BY created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_ticket(ticket_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
    if not row:
        conn.close()
        return None
    ticket = dict(row)
    notes = conn.execute(
        "SELECT note_text, created_at FROM notes WHERE ticket_id=? ORDER BY created_at ASC",
        (ticket_id,)
    ).fetchall()
    ticket["notes"] = [dict(n) for n in notes]
    conn.close()
    return ticket

def update_ticket(ticket_id, status=None, note=None):
    conn = get_conn()
    now = datetime.utcnow().isoformat()
    if status:
        conn.execute(
            "UPDATE tickets SET status=?, updated_at=? WHERE ticket_id=?",
            (status, now, ticket_id)
        )
    if note:
        conn.execute(
            "INSERT INTO notes (ticket_id, note_text, created_at) VALUES (?, ?, ?)",
            (ticket_id, note, now)
        )
    conn.commit()
    conn.close()
    return {"success": True, "updated_at": now}

# Auto-init on import
init_db()
