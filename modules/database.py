"""
NyayaSathi - Database Module
SQLite-backed storage for user queries, analyses, saved complaint drafts, and evidence checklists.
Stores only minimal operational data locally without harvesting sensitive PII.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nyayasathi.db")


def get_connection():
    """Returns a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Analyses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        language TEXT NOT NULL,
        category_id TEXT NOT NULL,
        category_name TEXT NOT NULL,
        problem_text TEXT NOT NULL,
        summary TEXT NOT NULL,
        classification TEXT NOT NULL,
        urgency TEXT NOT NULL,
        provisions_json TEXT NOT NULL,
        action_plan_json TEXT NOT NULL,
        evidence_json TEXT NOT NULL,
        clarification_questions_json TEXT NOT NULL,
        ai_provider TEXT NOT NULL
    )
    """)

    # Complaint drafts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        title TEXT NOT NULL,
        category_id TEXT NOT NULL,
        complainant_name TEXT NOT NULL,
        opposite_party TEXT NOT NULL,
        incident_date TEXT,
        incident_location TEXT,
        dispute_amount TEXT,
        complaint_text TEXT NOT NULL,
        FOREIGN KEY (analysis_id) REFERENCES analyses (id) ON DELETE SET NULL
    )
    """)

    # Evidence checklist progress table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checklist_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER NOT NULL,
        item_id TEXT NOT NULL,
        item_text TEXT NOT NULL,
        is_completed INTEGER DEFAULT 0,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (analysis_id) REFERENCES analyses (id) ON DELETE CASCADE,
        UNIQUE(analysis_id, item_id)
    )
    """)

    # Cases table for full conversation sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        title TEXT NOT NULL,
        category_id TEXT,
        urgency TEXT,
        messages_json TEXT NOT NULL,
        analysis_id INTEGER,
        FOREIGN KEY (analysis_id) REFERENCES analyses (id) ON DELETE SET NULL
    )
    """)

    # Safe migration: ensure user_id column exists if table was created previously without it
    try:
        cursor.execute("ALTER TABLE cases ADD COLUMN user_id INTEGER")
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute("ALTER TABLE complaints ADD COLUMN user_id INTEGER")
    except sqlite3.OperationalError:
        pass  # Column already exists


    conn.commit()
    conn.close()


def save_analysis(
    language: str,
    category_id: str,
    category_name: str,
    problem_text: str,
    summary: str,
    classification: str,
    urgency: str,
    provisions: List[Dict[str, Any]],
    action_plan: List[Dict[str, Any]],
    evidence: List[Dict[str, Any]],
    clarification_questions: List[str],
    ai_provider: str = "Hybrid-RAG"
) -> int:
    """Saves a newly generated legal analysis to SQLite."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO analyses (
        created_at, language, category_id, category_name, problem_text,
        summary, classification, urgency, provisions_json, action_plan_json,
        evidence_json, clarification_questions_json, ai_provider
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now,
        language,
        category_id,
        category_name,
        problem_text,
        summary,
        classification,
        urgency,
        json.dumps(provisions, ensure_ascii=False),
        json.dumps(action_plan, ensure_ascii=False),
        json.dumps(evidence, ensure_ascii=False),
        json.dumps(clarification_questions, ensure_ascii=False),
        ai_provider
    ))

    analysis_id = cursor.lastrowid

    # Seed initial checklist items
    for idx, ev in enumerate(evidence):
        item_key = f"ev_{idx}"
        cursor.execute("""
        INSERT OR IGNORE INTO checklist_items (analysis_id, item_id, item_text, is_completed, updated_at)
        VALUES (?, ?, ?, 0, ?)
        """, (analysis_id, item_key, ev.get("item", str(ev)), now))

    conn.commit()
    conn.close()
    return analysis_id


def get_recent_analyses(limit: int = 10) -> List[Dict[str, Any]]:
    """Fetches the latest analyses for dashboard display."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, created_at, language, category_id, category_name, problem_text, summary, classification, urgency, ai_provider
    FROM analyses
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_analysis_by_id(analysis_id: int) -> Optional[Dict[str, Any]]:
    """Loads a full analysis and its parsed JSON objects."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    data = dict(row)
    data["provisions"] = json.loads(data.get("provisions_json", "[]"))
    data["action_plan"] = json.loads(data.get("action_plan_json", "[]"))
    data["evidence"] = json.loads(data.get("evidence_json", "[]"))
    data["clarification_questions"] = json.loads(data.get("clarification_questions_json", "[]"))
    return data


def save_complaint(
    analysis_id: Optional[int],
    title: str,
    category_id: str,
    complainant_name: str,
    opposite_party: str,
    incident_date: str,
    incident_location: str,
    dispute_amount: str,
    complaint_text: str,
    user_id: Optional[int] = None
) -> int:
    """Saves or updates a complaint letter draft."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO complaints (
        analysis_id, user_id, created_at, updated_at, title, category_id,
        complainant_name, opposite_party, incident_date, incident_location,
        dispute_amount, complaint_text
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        analysis_id, user_id, now, now, title, category_id,
        complainant_name, opposite_party, incident_date, incident_location,
        dispute_amount, complaint_text
    ))

    complaint_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return complaint_id


def update_complaint_text(complaint_id: int, new_text: str):
    """Updates the text content of a complaint draft."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE complaints
    SET complaint_text = ?, updated_at = ?
    WHERE id = ?
    """, (new_text, now, complaint_id))
    conn.commit()
    conn.close()


def get_recent_complaints(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieves recent complaint drafts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, analysis_id, created_at, updated_at, title, category_id, complainant_name, opposite_party, dispute_amount, complaint_text
    FROM complaints
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_complaint_by_id(complaint_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single complaint draft."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_checklist_item(analysis_id: int, item_id: str, is_completed: bool):
    """Toggles completion state of a specific evidence item."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE checklist_items
    SET is_completed = ?, updated_at = ?
    WHERE analysis_id = ? AND item_id = ?
    """, (1 if is_completed else 0, now, analysis_id, item_id))
    conn.commit()
    conn.close()


def get_checklist_for_analysis(analysis_id: int) -> List[Dict[str, Any]]:
    """Fetches checklist items and their completion status for an analysis."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT item_id, item_text, is_completed
    FROM checklist_items
    WHERE analysis_id = ?
    ORDER BY id ASC
    """, (analysis_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_dashboard_stats() -> Dict[str, Any]:
    """Computes high-level statistics for the user dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM analyses")
    total_analyses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cursor.fetchone()[0]

    cursor.execute("""
    SELECT category_id, COUNT(*) as cnt
    FROM analyses
    GROUP BY category_id
    """)
    category_counts = {row["category_id"]: row["cnt"] for row in cursor.fetchall()}

    cursor.execute("""
    SELECT COUNT(*) FROM checklist_items WHERE is_completed = 1
    """)
    completed_evidence = cursor.fetchone()[0]

    conn.close()
    return {
        "total_analyses": total_analyses,
        "total_complaints": total_complaints,
        "category_counts": category_counts,
        "completed_evidence": completed_evidence
    }


def save_case(title: str, messages: List[Dict[str, Any]], category_id: str = "general", urgency: str = "GREEN", analysis_id: Optional[int] = None, user_id: Optional[int] = None) -> int:
    """Saves or updates a user case session with strict user_id association."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO cases (user_id, created_at, updated_at, title, category_id, urgency, messages_json, analysis_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, now, now, title, category_id, urgency, json.dumps(messages, ensure_ascii=False), analysis_id))

    case_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return case_id


def get_saved_cases(user_id: Optional[int] = None, limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieves saved case sessions isolated by user_id."""
    conn = get_connection()
    cursor = conn.cursor()
    if user_id is not None:
        cursor.execute("""
        SELECT id, user_id, created_at, updated_at, title, category_id, urgency, messages_json, analysis_id
        FROM cases
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """, (user_id, limit))
    else:
        cursor.execute("""
        SELECT id, user_id, created_at, updated_at, title, category_id, urgency, messages_json, analysis_id
        FROM cases
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    cases = []
    for r in rows:
        d = dict(r)
        try:
            d["messages"] = json.loads(d.get("messages_json", "[]"))
        except Exception:
            d["messages"] = []
        cases.append(d)
    return cases


def get_case_by_id(case_id: int, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Loads a single case session by ID and verifies user ownership."""
    conn = get_connection()
    cursor = conn.cursor()
    if user_id is not None:
        cursor.execute("SELECT * FROM cases WHERE id = ? AND user_id = ?", (case_id, user_id))
    else:
        cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    try:
        d["messages"] = json.loads(d.get("messages_json", "[]"))
    except Exception:
        d["messages"] = []
    return d


def delete_case(case_id: int, user_id: Optional[int] = None):
    """Deletes a saved case session only if owned by user."""
    conn = get_connection()
    cursor = conn.cursor()
    if user_id is not None:
        cursor.execute("DELETE FROM cases WHERE id = ? AND user_id = ?", (case_id, user_id))
    else:
        cursor.execute("DELETE FROM cases WHERE id = ?", (case_id,))
    conn.commit()
    conn.close()




# Automatically create tables on module import
init_db()
