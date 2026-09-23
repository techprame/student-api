# Student Management API

A FastAPI + SQLAlchemy (SQLite) CRUD API for students and products, with JWT authentication.

## Project structure

```
app/
├── main.py            # FastAPI app, exception handlers, router registration
├── database.py        # Engine, session, get_db dependency
├── models.py          # SQLAlchemy models
├── schemas.py         # Pydantic request/response schemas
├── routes/            # HTTP endpoints
├── controllers/       # Request handling logic
├── services/          # Business logic
├── repositories/      # Database queries
└── utils/security.py  # Password hashing, JWT creation/validation
```

Request flow: `routes → controllers → services → repositories → database`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set a real SECRET_KEY
```

## Run

```bash
uvicorn app.main:app --reload --env-file .env
```

- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs

The SQLite database file `students.db` is created automatically on first run and is not committed.
