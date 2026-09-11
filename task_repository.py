import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            [
                ("Learn FastAPI", False),
                ("Build Task API", False),
                ("Push to GitHub", False),
            ]
        )

    conn.commit()
    conn.close()


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks ORDER BY id")
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
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {"id": row[0], "title": row[1], "done": bool(row[2])}


def insert_task(title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
        (title, False)
    )
    new_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return {"id": new_id, "title": title, "done": False}


def update_task_row(task_id, title, done):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s",
        (title, done, task_id)
    )
    rows_updated = cursor.rowcount
    conn.commit()
    conn.close()

    if rows_updated == 0:
        return None

    return {"id": task_id, "title": title, "done": done}


def delete_task_row(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    rows_deleted = cursor.rowcount
    conn.commit()
    conn.close()

    return rows_deleted > 0
