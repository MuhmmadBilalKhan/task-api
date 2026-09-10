import sqlite3

DB_FILE = "tasks.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    # Connect to database
    # If tasks.db does not exist, SQLite creates it automatically
    conn = get_connection()
    cursor = conn.cursor()

    # Create tasks table if it does not already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    # Check how many tasks already exist
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    # Add seed tasks ONLY if database is empty
    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", 0),
                ("Build Task API", 0),
                ("Push to GitHub", 0),
            ]
        )

    # Save changes
    conn.commit()

    # Close database connection
    conn.close()


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        })
    return result


def get_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {"id": row[0], "title": row[1], "done": bool(row[2])}


def insert_task(title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, 0)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"id": new_id, "title": title, "done": False}


def update_task_row(task_id, title, done):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (title, int(done), task_id)
    )
    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()

    if rows_updated == 0:
        return None

    return {"id": task_id, "title": title, "done": done}


def delete_task_row(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()

    return rows_deleted > 0
