# db_manager.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Database connection parameters from environment variables
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER'), # CRITICAL: Ensure these are set in .env
    'password': os.getenv('MYSQL_PASSWORD'), # CRITICAL: Ensure these are set in .env
    'database': os.getenv('MYSQL_DATABASE'), # CRITICAL: Ensure these are set in .env
    'port': int(os.getenv('MYSQL_PORT', 3306)) # Ensure port is integer
}

# Check if critical DB_CONFIG values are None (not set in .env)
if not all([DB_CONFIG['user'], DB_CONFIG['password'], DB_CONFIG['database']]):
    print("CRITICAL ERROR: MySQL user, password, or database not set in .env file.")
    print("Please create a .env file with MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE.")
    # exit(1) # Optionally exit if not configured

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        print(f"Using config: host={DB_CONFIG['host']}, user={DB_CONFIG['user']}, db={DB_CONFIG['database']}, port={DB_CONFIG['port']}")
        if "Access denied" in str(e):
            print("Hint: Check your MYSQL_USER and MYSQL_PASSWORD in the .env file.")
        elif "Unknown database" in str(e):
            print(f"Hint: Ensure the database '{DB_CONFIG['database']}' exists in MySQL.")
        return None

def init_db():
    """Initializes the database and creates the reminders table if it doesn't exist."""
    conn = get_db_connection()
    if not conn:
        print("DB Init: Could not connect to database. Table creation skipped.")
        return

    cursor = conn.cursor()
    try:
        # Use DATETIME for due_date and created_at
        # Use TEXT for task as it can be variable length
        # Use BOOLEAN (TINYINT(1) in MySQL) for flags
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task TEXT NOT NULL,
                due_date DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_reminded BOOLEAN DEFAULT FALSE,
                is_done BOOLEAN DEFAULT FALSE,
                INDEX idx_due_date_reminded_done (due_date, is_reminded, is_done),
                INDEX idx_is_done (is_done)
            ) ENGINE=InnoDB;
        """)
        conn.commit()
        print("DB: Table 'reminders' checked/created successfully in MySQL.")
    except Error as e:
        print(f"DB Error during table creation: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def add_reminder(task: str, due_date: datetime):
    """Adds a new reminder to the database."""
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    # due_date is already a Python datetime object, mysql.connector handles conversion
    sql = "INSERT INTO reminders (task, due_date) VALUES (%s, %s)"
    val = (task, due_date)
    try:
        cursor.execute(sql, val)
        conn.commit()
        reminder_id = cursor.lastrowid
        print(f"DB: Reminder '{task}' for {due_date} added with ID {reminder_id}.")
        return reminder_id
    except Error as e:
        print(f"DB Error adding reminder: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_due_reminders():
    """Retrieves reminders that are due and not yet reminded or done."""
    conn = get_db_connection()
    if not conn:
        return []

    # Fetch as dictionaries for easier access by column name
    cursor = conn.cursor(dictionary=True)
    now = datetime.now()
    sql = """
        SELECT id, task, due_date FROM reminders
        WHERE due_date <= %s AND is_reminded = FALSE AND is_done = FALSE
        ORDER BY due_date ASC
    """
    try:
        cursor.execute(sql, (now,))
        reminders = cursor.fetchall() # List of dictionaries
        return reminders
    except Error as e:
        print(f"DB Error getting due reminders: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def mark_as_reminded(reminder_id: int):
    """Marks a reminder as having been reminded."""
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()
    sql = "UPDATE reminders SET is_reminded = TRUE WHERE id = %s"
    try:
        cursor.execute(sql, (reminder_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"DB: Reminder ID {reminder_id} marked as reminded.")
        else:
            print(f"DB Warning: No reminder found with ID {reminder_id} to mark as reminded.")
    except Error as e:
        print(f"DB Error marking as reminded: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def mark_as_done(reminder_id: int):
    """Marks a reminder as done (and also as reminded)."""
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()
    sql = "UPDATE reminders SET is_done = TRUE, is_reminded = TRUE WHERE id = %s"
    try:
        cursor.execute(sql, (reminder_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"DB: Reminder ID {reminder_id} marked as done.")
        else:
            print(f"DB Warning: No reminder found with ID {reminder_id} to mark as done.")
    except Error as e:
        print(f"DB Error marking as done: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_active_reminders():
    """Retrieves all reminders that are not yet done."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True) # Fetch as dictionaries
    sql = """
        SELECT id, task, due_date FROM reminders
        WHERE is_done = FALSE
        ORDER BY due_date ASC
    """
    try:
        cursor.execute(sql)
        reminders = cursor.fetchall()
        return reminders
    except Error as e:
        print(f"DB Error getting active reminders: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    print("Attempting to initialize MySQL database schema...")
    init_db()
    print("Database initialization attempt complete.")