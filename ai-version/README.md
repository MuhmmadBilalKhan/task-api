# Task API (AI-generated version)

A simple CRUD To-Do Task API built with Python and FastAPI. Tasks are stored in memory and reset when the server restarts.

## Install

```
pip install -r requirements.txt
```

## Run

```
uvicorn main:app --reload
```

The server starts at http://localhost:8000

## Use the API

- GET / — API info
- GET /health — health check
- GET /tasks — list all tasks
- GET /tasks/{id} — get one task
- POST /tasks — create a task (body: {"title": "..."})
- PUT /tasks/{id} — update a task (body: {"title": "...", "done": true})
- DELETE /tasks/{id} — delete a task

## Swagger UI

Open http://localhost:8000/docs to test every endpoint interactively.
