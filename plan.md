# Plan — Notes API (Project 03)

> This plan follows the exact implementation tasks, constraints, and rules defined in `project.md`. Nothing has been added, removed, or reworded beyond what is necessary to express the plan as actionable steps.

---

## Tech Stack (locked)

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| Framework | FastAPI |
| Validation | Pydantic v2 (bundled with FastAPI) |
| Server | Uvicorn (ASGI) |
| Testing | pytest + httpx |
| VCS | Git with feature branches |

### Explicitly forbidden

- Any database or ORM (SQLAlchemy, SQLite, etc.)
- Authentication middleware
- Any frontend
- Docker

---

## Project Structure (exact)

```
Note_API/
├── README.md
├── requirements.txt
├── .gitignore
└── app/
    ├── main.py
    ├── models/
    │   └── note.py
    ├── routes/
    │   └── notes.py
    ├── services/
    │   └── note_service.py
    ├── storage/
    │   └── in_memory.py
    └── tests/
        ├── conftest.py
        └── test_notes.py
```

---

## Task 1 — Project Setup

**Branch:** `main` (initial commit)

| # | Step | Detail |
|---|---|---|
| 1 | Create virtual environment | `python -m venv venv` |
| 2 | Activate it | `venv\Scripts\activate` (Windows) |
| 3 | Install dependencies | `pip install fastapi uvicorn pytest httpx` |
| 4 | Freeze deps | `pip freeze > requirements.txt` |
| 5 | Create `app/main.py` | Minimal FastAPI app: import FastAPI, create `app = FastAPI()`, add a root `/` health-check placeholder |
| 6 | Verify server starts | `uvicorn app.main:app --reload` → visit `http://localhost:8000/docs` |
| 7 | Create `.gitignore` | Python + venv entries (`venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`) |
| 8 | Init Git & commit | `git init && git add . && git commit -m "chore: initialize FastAPI project"` |

**Commit message:** `"chore: initialize FastAPI project"`

---

## Task 2 — Define Your Models

**Branch:** `feature/note-models`

Create `app/models/note.py` with three Pydantic v2 models:

| Model | Fields | Notes |
|---|---|---|
| `NoteCreate` | `title: str` (required), `content: str` (required) | What the client sends to create a note |
| `NoteUpdate` | `title: Optional[str]` , `content: Optional[str]` | Both optional — allows partial update via PUT |
| `NoteResponse` | `id: str`, `title: str`, `content: str`, `created_at: datetime`, `updated_at: datetime` | What the API returns to the client |

- Add `__init__.py` files in `app/` and `app/models/` to make them packages.

**Commit message:** `"feat: define note Pydantic models"`

---

## Task 3 — Build the In-Memory Store

**Branch:** `feature/in-memory-store`

Create `app/storage/in_memory.py` with a `NoteStore` class:

| Method | Behavior |
|---|---|
| `create(title, content) → dict` | Generate UUID via `uuid.uuid4()`, record `created_at` and `updated_at` with `datetime.utcnow()`, store in internal `dict` keyed by ID, return the note dict |
| `get(note_id) → dict or None` | Lookup by ID, return `None` if missing |
| `get_all() → list[dict]` | Return all notes as a list |
| `update(note_id, title?, content?) → dict or None` | Update only provided fields, refresh `updated_at`, return updated note or `None` |
| `delete(note_id) → bool` | Remove from dict, return `True` if existed, `False` otherwise |

- This class must have **no knowledge of FastAPI or HTTP**.
- Add `__init__.py` in `app/storage/`.

**Commit message:** `"feat: implement in-memory note store"`

---

## Task 4 — Build the Service Layer

**Branch:** (continue on `feature/in-memory-store` or create new)

Create `app/services/note_service.py` with a `NoteService` class:

| Responsibility | Detail |
|---|---|
| Uses `NoteStore` | All CRUD operations delegate to the store |
| Raises Python exceptions | e.g., a custom `NoteNotFoundError` when a note ID doesn't exist |
| Does **not** import FastAPI | No HTTP-level concerns here |

- Create a custom exception class (e.g., `NoteNotFoundError`) in `app/services/` or a shared `app/exceptions.py`.
- Add `__init__.py` in `app/services/`.

**Commit message:** `"feat: implement note service layer"`

---

## Task 5 — Build the Routes

**Branch:** `feature/notes-routes`

Create `app/routes/notes.py` with an `APIRouter`:

| Endpoint | Method | Success Code | Failure Code |
|---|---|---|---|
| `/notes` | POST | 201 | 422 (validation) |
| `/notes` | GET | 200 | — |
| `/notes/{id}` | GET | 200 | 404 |
| `/notes/{id}` | PUT | 200 | 404 / 422 |
| `/notes/{id}` | DELETE | 204 | 404 |

Each route must:

1. Accept and validate input via the Pydantic models from Task 2.
2. Call the service layer from Task 4.
3. Return the correct HTTP status code.
4. Catch service-layer exceptions and translate them to HTTP error responses.

Register the router in `app/main.py`:

```python
from app.routes.notes import router as notes_router
app.include_router(notes_router)
```

- Add `__init__.py` in `app/routes/`.

**Commit message:** `"feat: implement notes CRUD routes"`

---

## Task 6 — Standardize Error Responses

**Branch:** `feature/error-handling`

### Error response format (exact)

**Business errors:**

```json
{
  "error": "note_not_found",
  "message": "Note with id '...' does not exist",
  "field": null
}
```

**Validation errors:**

```json
{
  "error": "validation_error",
  "message": "Invalid input",
  "field": "title",
  "detail": "Title must be at least 3 characters"
}
```

### Implementation steps

1. Create an `ErrorResponse` Pydantic model with fields: `error`, `message`, `field` (optional), `detail` (optional).
2. Add a FastAPI exception handler for `NoteNotFoundError` → return 404 with the standard body.
3. Override FastAPI's default `RequestValidationError` handler → return 422 with field-level detail in the standard body.
4. Add a catch-all handler for `Exception` → return 500 with a generic message, **never** expose stack traces.
5. Handle malformed JSON → return 400 with consistent error response.

**Commit message:** `"feat: standardize error response format"`

---

## Task 7 — Add Logging

**Branch:** `feature/logging`

Use Python's built-in `logging` module.

| What to log | Detail |
|---|---|
| Every request | Method, path, status code |
| Every error | Context: what was being attempted, what failed |
| **Never** log | Full request bodies (may contain sensitive data) |

Implementation: add a FastAPI middleware that logs request method, path, and response status code for every request.

**Commit message:** `"feat: add request and error logging"`

---

## Task 8 — Write API Tests

**Branch:** `feature/tests`

Create `app/tests/conftest.py`:

- Set up a `TestClient` fixture from `fastapi.testclient` (backed by `httpx`).
- Ensure storage is reset between tests.

Create `app/tests/test_notes.py` with the following **required** integration test cases:

| # | Test case | Expected |
|---|---|---|
| 1 | `POST /notes` with valid data | 201 + note in response |
| 2 | `POST /notes` with empty title | 422 + validation error |
| 3 | `POST /notes` with missing content | 422 + validation error |
| 4 | `GET /notes` with no notes | 200 + empty list |
| 5 | `GET /notes` with notes | 200 + list of notes |
| 6 | `GET /notes/{id}` with valid id | 200 + note |
| 7 | `GET /notes/{id}` with invalid id | 404 + error |
| 8 | `PUT /notes/{id}` with valid data | 200 + updated note |
| 9 | `PUT /notes/{id}` with non-existent id | 404 + error |
| 10 | `DELETE /notes/{id}` with valid id | 204 |
| 11 | `DELETE /notes/{id}` with non-existent id | 404 + error |

Run: `pytest --tb=short -v`

**Commit message:** `"test: add notes API test suite"`

---

## Task 9 — Validation Rules

**Branch:** (continue on `feature/tests` or a dedicated branch)

Add these rules in the Pydantic models (or service layer):

| Field | Rule |
|---|---|
| `title` | Required, 3–200 characters, strip leading/trailing whitespace |
| `content` | Required, 1–10,000 characters, strip leading/trailing whitespace |

When validation fails → return **422** with field-level error message in the standard error format.

**Commit message:** `"feat: add field-level validation rules"`

---

## Task 10 — Documentation and Review

**Branch:** `main` (final merge)

| # | Step |
|---|---|
| 1 | Write `README.md`: what the API does, how to run it, all endpoints, example requests/responses |
| 2 | Verify `http://localhost:8000/docs` is usable and accurate |
| 3 | Run `pytest --tb=short -v` — all tests must pass |
| 4 | Remove any dead/commented-out code |

**Commit message:** `"docs: add API documentation and README"`

---

## Unit Tests — Service Layer (required, ≥ 3)

These go alongside the integration tests (Task 8) or in a separate `test_note_service.py`:

| # | Test | Assertion |
|---|---|---|
| 1 | Creating a note generates an ID and timestamps | `id`, `created_at`, `updated_at` are present and valid |
| 2 | Getting a non-existent note raises `NoteNotFoundError` | Exception is raised |
| 3 | Updating a note updates `updated_at` but not `created_at` | `updated_at` changes, `created_at` stays the same |

---

## Debugging Exercise

After all tasks are complete:

1. In `note_service.py`, introduce a bug: when updating a note, write the update to a **new variable** that is immediately discarded (so the store is never actually mutated).
2. Write/run the `PUT /notes/{id}` test that verifies the note was actually updated → it should **fail**.
3. Use the test failure + logging to identify the root cause.
4. Fix the bug and confirm the test passes.

---

## Git Workflow

- **Remote:** `https://github.com/AhmedMelliti9/Note_API.git`
- Use feature branches throughout.
- **Never merge a branch that has failing tests.**

### Branch plan

| Branch | Covers |
|---|---|
| `feature/note-models` | Task 2 |
| `feature/in-memory-store` | Tasks 3–4 |
| `feature/notes-routes` | Task 5 |
| `feature/error-handling` | Task 6 |
| `feature/logging` | Task 7 |
| `feature/tests` | Tasks 8–9 |

---

## Error Handling Summary (exact)

| Scenario | HTTP Status | Response Body |
|---|---|---|
| Note not found | 404 | `{"error": "note_not_found", "message": "..."}` |
| Title too short | 422 | `{"error": "validation_error", "field": "title", ...}` |
| Title too long | 422 | `{"error": "validation_error", "field": "title", ...}` |
| Content missing | 422 | `{"error": "validation_error", "field": "content", ...}` |
| Malformed JSON body | 400 | Consistent error response |
| Unhandled exception | 500 | Generic message — no stack trace exposed |

---

## Security Checklist

- [ ] All string inputs validated for length and content
- [ ] Leading/trailing whitespace stripped from all string inputs
- [ ] Pydantic validators run automatically on every request
- [ ] No Python traceback or exception message ever returned in an HTTP response
- [ ] Full errors logged server-side; generic message returned to client

---

## Definition of Done

- [ ] All functional requirements (FR-01 through FR-08) are met
- [ ] All routes return the correct HTTP status codes
- [ ] Validation errors include field-level details
- [ ] Error responses never expose stack traces
- [ ] All API tests pass: `pytest`
- [ ] At least 3 unit tests for the service layer pass
- [ ] Logging records method, path, and status code for every request
- [ ] `README.md` documents all endpoints with example requests and responses
- [ ] No commented-out code
- [ ] Feature branches used throughout
- [ ] Debugging exercise completed and answers written

---

## Stretch Goals (optional, not required)

- Add pagination to `GET /notes` (limit + offset query parameters)
- Add a search endpoint: `GET /notes?search=keyword`
- Add `PATCH /notes/{id}` (partial update — only provided fields change)
- Add a health check endpoint: `GET /health` → `{"status": "ok"}`

### Do NOT implement

- Authentication
- A database
- Docker
- A frontend
