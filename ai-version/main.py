from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build Task API", "done": False},
    {"id": 3, "title": "Push to GitHub", "done": False},
]


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": "/tasks"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", status_code=201)
def create_task(payload: dict):
    title = payload.get("title")
    if not title or not str(title).strip():
        raise HTTPException(status_code=400, detail="Title is required")

    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: dict):
    if not payload:
        raise HTTPException(status_code=400, detail="Request body is empty")

    for task in tasks:
        if task["id"] == task_id:
            if "title" in payload:
                if not payload["title"] or not str(payload["title"]).strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = payload["title"]
            if "done" in payload:
                task["done"] = payload["done"]
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return
    raise HTTPException(status_code=404, detail="Task not found")
