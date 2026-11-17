"""
NyayaSathi - User Authentication & Session Security Module
Uses standard library hashlib.pbkdf2_hmac (SHA-256 with 200,000 iterations and cryptographic salt).
Provides secure password hashing, user registration/login, session verification, and user isolation.
"""

import hashlib
import os
import secrets
import sqlite3
from typing import Optional, Dict, Any, Tuple
from modules.database import get_connection

def hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[str, str]:
    """
    Hashes a password using PBKDF2-HMAC-SHA256 with a 16-byte random salt and 200,000 iterations.
    Returns (hex_hash, hex_salt).
    """
    if salt is None:
        salt = secrets.token_bytes(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 200000)
    return hashed.hex(), salt.hex()


def verify_password(stored_hash: str, stored_salt_hex: str, provided_password: str) -> bool:
    """Verifies a password attempt in constant time to prevent timing attacks."""
    salt = bytes.fromhex(stored_salt_hex)
    attempt_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 200000).hex()
    return secrets.compare_digest(stored_hash, attempt_hash)


def init_auth_tables():
    """Initializes users and login_attempts tables."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        password_salt TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_login TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        attempt_time TEXT NOT NULL,
        success INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()


def create_user(username: str, password: str, full_name: str = "") -> Tuple[bool, str]:
    """Registers a new user with hashed credentials."""
    username = username.strip().lower()
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    pwd_hash, salt_hex = hash_password(password)
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO users (username, full_name, password_hash, password_salt, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (username, full_name or username.capitalize(), pwd_hash, salt_hex, now))
        conn.commit()
        conn.close()
        return True, "User account created successfully."
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username is already registered."
    except Exception as e:
        conn.close()
        return False, f"Database error: {e}"


def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Validates username and password against SQLite.
    Returns (success_bool, user_dict, message).
    """
    username = username.strip().lower()
    if not username or not password:
        return False, None, "Please enter both username and password."

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, password_hash, password_salt FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not row:
        cursor.execute("INSERT INTO login_attempts (username, attempt_time, success) VALUES (?, ?, 0)", (username, now))
        conn.commit()
        conn.close()
        return False, None, "Invalid username or password."

    stored_hash = row["password_hash"]
    stored_salt = row["password_salt"]

    if verify_password(stored_hash, stored_salt, password):
        cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, row["id"]))
        cursor.execute("INSERT INTO login_attempts (username, attempt_time, success) VALUES (?, ?, 1)", (username, now))
        conn.commit()
        user_info = {
            "id": row["id"],
            "username": row["username"],
            "full_name": row["full_name"]
        }
        conn.close()
        return True, user_info, "Login successful."
    else:
        cursor.execute("INSERT INTO login_attempts (username, attempt_time, success) VALUES (?, ?, 0)", (username, now))
        conn.commit()
        conn.close()
        return False, None, "Invalid username or password."


# Initialize tables on load
init_auth_tables()
