from supabase_client import supabase
from fastapi import FastAPI, HTTPException
from task_repository import (
    init_db,
    get_all_tasks,
    get_task_by_id,
    insert_task,
    update_task_row,
    delete_task_row,
)

app = FastAPI()

# Run database setup when application starts
init_db()


# NOTE: this old in-memory list is only used by filter/page/stats/reset for now.
# All real CRUD (GET/POST/PUT/DELETE on /tasks) goes through task_repository.py.
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build Task API", "done": False},
    {"id": 3, "title": "Push to GitHub", "done": False},
]


@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return get_all_tasks()


# NOTE: these two must come BEFORE /tasks/{task_id},
# otherwise FastAPI tries to parse "filter" or "page" as a task_id.

@app.get("/tasks/filter")
def filter_tasks(done: bool | None = None, search: str | None = None):
    result = tasks

    if done is not None:
        result = [t for t in result if t["done"] == done]

    if search is not None:
        result = [
            t for t in result
            if search.lower() in t["title"].lower()
        ]

    return result


@app.get("/tasks/page")
def paginate_tasks(limit: int = 10, offset: int = 0):
    return tasks[offset: offset + limit]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201)
def create_task(new_task: dict):
    title = new_task.get("title", "")

    if not isinstance(title, str) or not title.strip():
        raise HTTPException(
            status_code=400,
            detail="title is required and cannot be empty"
        )

    return insert_task(title)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: dict):
    title = updated_task.get("title", "")

    if not isinstance(title, str) or not title.strip():
        raise HTTPException(
            status_code=400,
            detail="title is required and cannot be empty"
        )

    done = updated_task.get("done", False)

    if not isinstance(done, bool):
        raise HTTPException(
            status_code=400,
            detail="done must be true or false"
        )

    result = update_task_row(task_id, title, done)

    if result is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return result


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = delete_task_row(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return


@app.get("/stats")
def get_stats():
    total = len(tasks)
    done_count = sum(
        1 for t in tasks
        if t["done"]
    )

    return {
        "total": total,
        "done": done_count,
        "open": total - done_count
    }


@app.post("/reset")
def reset_tasks():
    global tasks

    tasks = [
        {"id": 1, "title": "Learn FastAPI", "done": False},
        {"id": 2, "title": "Build Task API", "done": False},
        {"id": 3, "title": "Push to GitHub", "done": False},
    ]

    return {"message": "Tasks reset to default"}
