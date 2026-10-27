import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "quality_prediction.db"

def connection():
    con = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA busy_timeout = 30000")
    con.execute("PRAGMA journal_mode = WAL")
    return con

def init_db():
    with connection() as con:
        con.executescript('''
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
          password_hash TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, product_id TEXT, temperature REAL, voltage REAL,
          current REAL, weight REAL, pressure REAL, humidity REAL, machine_speed REAL, created_at TEXT DEFAULT CURRENT_TIMESTAMP, user_id INTEGER);
        CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY, product_id TEXT, quality_score REAL, prediction TEXT,
          reason TEXT, suggested_action TEXT, prediction_date TEXT DEFAULT CURRENT_TIMESTAMP, user_id INTEGER);
        ''')

def add_prediction(user_id, row, result):
    with connection() as con:
        con.execute("INSERT INTO products(product_id,temperature,voltage,current,weight,pressure,humidity,machine_speed,user_id) VALUES(?,?,?,?,?,?,?,?,?)",
          (row["Product_ID"], *[float(row[k]) for k in ["Temperature","Voltage","Current","Weight","Pressure","Humidity","Machine_Speed"]], user_id))
        con.execute("INSERT INTO predictions(product_id,quality_score,prediction,reason,suggested_action,user_id) VALUES(?,?,?,?,?,?)",
          (row["Product_ID"], float(result["Quality_Score"]), result["Prediction"], result["Reason"], result["Suggested_Action"], user_id))

def add_predictions(user_id, results):
    """Persist a bulk result in one short SQLite transaction."""
    products=[]; predictions=[]
    for row in results.to_dict("records"):
        products.append((row["Product_ID"], *[float(row[key]) for key in ["Temperature","Voltage","Current","Weight","Pressure","Humidity","Machine_Speed"]], user_id))
        predictions.append((row["Product_ID"], float(row["Quality_Score"]), row["Prediction"], row["Reason"], row["Suggested_Action"], user_id))
    with connection() as con:
        con.executemany("INSERT INTO products(product_id,temperature,voltage,current,weight,pressure,humidity,machine_speed,user_id) VALUES(?,?,?,?,?,?,?,?,?)", products)
        con.executemany("INSERT INTO predictions(product_id,quality_score,prediction,reason,suggested_action,user_id) VALUES(?,?,?,?,?,?)", predictions)

def history(user_id):
    with connection() as con:
        return [dict(r) for r in con.execute("SELECT * FROM predictions WHERE user_id=? ORDER BY prediction_date DESC", (user_id,))]

def user_by_email(email):
    with connection() as con: 
        r=con.execute("SELECT * FROM users WHERE email=?", (email.lower(),)).fetchone(); return dict(r) if r else None

def user_by_id(user_id):
    """Fetch the current account from the canonical SQLite database."""
    with connection() as con:
        r=con.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone(); return dict(r) if r else None

def create_user(name,email,password_hash):
    with connection() as con: con.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)", (name,email.lower(),password_hash))

def update_name(user_id,name):
    with connection() as con: con.execute("UPDATE users SET name=? WHERE id=?", (name,user_id))
