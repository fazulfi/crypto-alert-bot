# services/alerts_db.py
import sqlite3
from datetime import datetime
import os

DB_PATH = os.getenv('ALERTS_DB', 'alerts.db')
_conn = None

def _connect():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return _conn

def init_db():
    c = _connect().cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            symbol TEXT,
            direction TEXT,
            price REAL,
            triggered INTEGER DEFAULT 0,
            created_at TEXT
        )
    ''')
    _connect().commit()

def add_alert(chat_id, symbol, direction, price):
    cur = _connect().cursor()
    created = datetime.utcnow().isoformat()
    cur.execute('INSERT INTO alerts (chat_id,symbol,direction,price,created_at) VALUES (?,?,?,?,?)',
                (str(chat_id), symbol, direction, float(price), created))
    _connect().commit()
    return cur.lastrowid

def get_alerts_by_chat(chat_id):
    cur = _connect().cursor()
    cur.execute('SELECT id,symbol,direction,price,triggered,created_at FROM alerts WHERE chat_id=? ORDER BY id DESC', (str(chat_id),))
    return cur.fetchall()

def get_pending_alerts():
    cur = _connect().cursor()
    cur.execute('SELECT id,chat_id,symbol,direction,price FROM alerts WHERE triggered=0')
    return cur.fetchall()

def mark_triggered(aid):
    cur = _connect().cursor()
    cur.execute('UPDATE alerts SET triggered=1 WHERE id=?', (aid,))
    _connect().commit()

def delete_alert(aid, chat_id=None):
    cur = _connect().cursor()
    if chat_id:
        cur.execute('DELETE FROM alerts WHERE id=? AND chat_id=?', (aid, str(chat_id)))
    else:
        cur.execute('DELETE FROM alerts WHERE id=?', (aid,))
    _connect().commit()
