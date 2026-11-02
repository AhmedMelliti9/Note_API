# Project 03 — Notes API

## Problem Statement

A developer team uses a shared notes service to capture quick technical notes, decisions, and links during meetings. The notes need to be accessible via an API so that different tools (CLI, browser extension, future mobile app) can use them.

You are building the backend API for this notes service. The API will store notes in memory for now — persistence comes in a later project.

Other developers on the team will consume your API. This means your responses must be consistent, your errors must be informative, and your behavior must be predictable.

---

## Functional Requirements

```
FR-01: Clients can create a note with a title and content.
FR-02: Clients can retrieve a list of all notes.
FR-03: Clients can retrieve a single note by its ID.
FR-04: Clients can update an existing note's title or content.
FR-05: Clients can delete a note by its ID.
FR-06: Each note has an auto-generated unique ID, a creation timestamp, and a last-updated timestamp.
FR-07: The API rejects invalid input with a structured error response that identifies which field is invalid.
FR-08: The API returns a 404 error when a requested note does not exist.
```

---

## Non-Functional Requirements

```
NFR-01: All error responses follow a consistent JSON structure.
NFR-02: The API logs every request with method, path, and status code.
NFR-03: Validation errors clearly identify which field failed and why.
NFR-04: The API never exposes internal implementation details (stack traces, memory addresses) in error responses.
NFR-05: The codebase is structured so that routes, models, and business logic are in separate files.
```

---

## Technical Requirements

### You must use:

- Python 3.11+
- FastAPI
- Pydantic v2 (bundled with FastAPI)
- Uvicorn (ASGI server)
- pytest + httpx (for API tests)
- Git with feature branches

### You must NOT use:

- A database of any kind — use a Python dict or list in memory
- SQLAlchemy or any ORM
- Authentication middleware
- Any frontend

### Why these constraints?

The purpose of this project is to understand the HTTP layer, not the persistence layer. Introducing a database now would split your attention. Databases come in Project 05.

### Installing dependencies:

Use a virtual environment:

```
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install fastapi uvicorn pytest httpx
pip freeze > requirements.txt
```

---

## HTTP Fundamentals — Read Before You Build

Before writing any code, you must understand these concepts. Look them up if you do not know them.

### HTTP Methods

| Method | Purpose | Notes |
|---|---|---|
| GET | Retrieve a resource | Must not change server state |
| POST | Create a new resource | Returns 201 on success |
| PUT | Replace an existing resource | Idempotent — same result if called twice |
| PATCH | Partially update a resource | Update only provided fields |
| DELETE | Remove a resource | Returns 204 on success (no body) |

### HTTP Status Codes

| Code | Meaning | When to use |
|---|---|---|
| 200 | OK | Successful GET or PATCH |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE (nothing to return) |
| 400 | Bad Request | The client sent malformed data |
| 404 | Not Found | The requested resource does not exist |
| 409 | Conflict | The request conflicts with current state |
| 422 | Unprocessable Entity | Validation failed on well-formed data |
| 500 | Internal Server Error | Something broke on the server |

You will use all of these at some point in this course. Learn what they mean now.

---

## Suggested Project Structure

```
03-simple-backend-api/
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

### Why this structure?

- `models/` holds Pydantic request/response models — the contracts of your API
- `routes/` holds FastAPI route definitions — what URLs exist and what HTTP methods they accept
- `services/` holds business logic — what happens when a request arrives
- `storage/` holds the in-memory data store — isolated so it can later be replaced with a real database
- Keeping these separated means you can change one layer without touching the others

---

## Implementation Tasks

### Task 1 — Project Setup

- Create a Python virtual environment
- Install dependencies
- Initialize a minimal FastAPI app in `main.py`
- Verify the server starts: `uvicorn app.main:app --reload`
- Visit `http://localhost:8000/docs` — FastAPI auto-generates documentation
- Add `.gitignore` (Python + venv)
- Initialize Git and make first commit

Commit: `"chore: initialize FastAPI project"`

---

### Task 2 — Define Your Models

In `app/models/note.py`, define Pydantic models for:

- `NoteCreate` — what a client sends to create a note (title + content only)
- `NoteUpdate` — what a client sends to update a note (both fields optional — why?)
- `NoteResponse` — what the API returns to the client (includes id, created_at, updated_at)

Think about which fields are required vs optional in each model and why.

Commit: `"feat: define note Pydantic models"`

---

### Task 3 — Build the In-Memory Store

In `app/storage/in_memory.py`, build a simple storage class that:

- Stores notes in a dict keyed by ID
- Supports: create, get by ID, get all, update, delete
- Generates a unique ID for each note (use `uuid.uuid4()`)
- Records `created_at` and `updated_at` timestamps (use `datetime.utcnow()`)

This class should have no knowledge of FastAPI or HTTP — it is just a data store.

Commit: `"feat: implement in-memory note store"`

---

### Task 4 — Build the Service Layer

In `app/services/note_service.py`, build a service that:

- Uses the storage class to perform operations
- Raises appropriate Python exceptions when things go wrong (e.g., note not found)
- Does not import FastAPI directly

Why a service layer? Because routes should only handle HTTP concerns (parsing request, building response). Business logic belongs one layer down.

Commit: `"feat: implement note service layer"`

---

### Task 5 — Build the Routes

In `app/routes/notes.py`, build FastAPI routes:

```
POST   /notes          → create a note (201)
GET    /notes          → list all notes (200)
GET    /notes/{id}     → get one note (200) or 404
PUT    /notes/{id}     → replace a note (200) or 404
DELETE /notes/{id}     → delete a note (204) or 404
```

Each route should:
- Accept and validate input via Pydantic
- Call the service layer
- Return the correct status code
- Handle exceptions from the service layer and return appropriate HTTP error responses

Register the router in `main.py`.

Commit: `"feat: implement notes CRUD routes"`

---

### Task 6 — Standardize Error Responses

All error responses must follow this structure:

```json
{
  "error": "note_not_found",
  "message": "Note with id '...' does not exist",
  "field": null
}
```

For validation errors:

```json
{
  "error": "validation_error",
  "message": "Invalid input",
  "field": "title",
  "detail": "Title must be at least 3 characters"
}
```

Implement a consistent error response model and use it everywhere.

Never return a raw Python exception or traceback to the client.

Commit: `"feat: standardize error response format"`

---

### Task 7 — Add Logging

Add structured logging using Python's built-in `logging` module.

Log every request: method, path, status code.

Log every error with its context (what was being attempted, what failed).

Do NOT log full request bodies (they may contain sensitive data in future projects).

Commit: `"feat: add request and error logging"`

---

### Task 8 — Write API Tests

In `tests/test_notes.py`, write pytest tests that test the API through HTTP (using the FastAPI test client).

Required test cases:

- `POST /notes` with valid data → 201 + note in response
- `POST /notes` with empty title → 422 + validation error in response
- `POST /notes` with missing content → 422 + validation error in response
- `GET /notes` with no notes → 200 + empty list
- `GET /notes` with notes → 200 + list of notes
- `GET /notes/{id}` with valid id → 200 + note
- `GET /notes/{id}` with invalid id → 404 + error
- `PUT /notes/{id}` with valid data → 200 + updated note
- `PUT /notes/{id}` with non-existent id → 404 + error
- `DELETE /notes/{id}` with valid id → 204
- `DELETE /notes/{id}` with non-existent id → 404 + error

Run tests: `pytest`

Commit: `"test: add notes API test suite"`

---

### Task 9 — Validation Rules

Add these server-side validation rules (in the Pydantic models or service layer):

- Title: required, 3–200 characters, strip leading/trailing whitespace
- Content: required, 1–10,000 characters, strip leading/trailing whitespace

When validation fails, return 422 with a field-level error message.

Commit: `"feat: add field-level validation rules"`

---

### Task 10 — Documentation and Review

- Write a `README.md` explaining: what the API does, how to run it, all available endpoints, and example requests/responses
- Verify `http://localhost:8000/docs` is usable and accurate
- Ensure all tests pass
- Remove any dead code

Commit: `"docs: add API documentation and README"`

---

## Error Handling Requirements

| Scenario | HTTP Status | Response Body |
|---|---|---|
| Note not found | 404 | `{"error": "note_not_found", "message": "..."}` |
| Title too short | 422 | `{"error": "validation_error", "field": "title", ...}` |
| Title too long | 422 | `{"error": "validation_error", "field": "title", ...}` |
| Content missing | 422 | `{"error": "validation_error", "field": "content", ...}` |
| Malformed JSON body | 400 | Consistent error response |
| Unhandled exception | 500 | Generic message — no stack trace exposed |

### Key concepts to understand:

**Expected business error:** "Note not found" — this is a predictable, handled scenario.

**Validation error:** "Title is too short" — the client sent invalid data.

**Infrastructure error:** The server ran out of memory — unexpected, should never reach the client as a traceback.

**Programming error:** A bug in your code — should log the full error server-side, return a generic 500 to the client.

---

## Testing Requirements

### Unit tests — service layer

Write at least 3 unit tests for `note_service.py` that test logic without HTTP:

- Creating a note generates an ID and timestamps
- Getting a non-existent note raises the expected exception
- Updating a note updates `updated_at` but not `created_at`

### Integration tests — API layer

Write all the API tests listed in Task 8 above using FastAPI's `TestClient`.

### Run all tests:

```
pytest --tb=short -v
```

All tests must pass before you consider the project complete.

---

## Git Requirements
push to this repo: 'https://github.com/AhmedMelliti9/Note_API.git' 

Continue using feature branches.

Suggested branches:

- `feature/note-models`
- `feature/in-memory-store`
- `feature/notes-routes`
- `feature/error-handling`
- `feature/logging`
- `feature/tests`

New rule this week:

**Do not merge a branch that has failing tests.**

---

## Security Requirements

**Input Validation (server-side)**

- All string inputs must be validated for length and content
- Strip leading/trailing whitespace from all string inputs
- Pydantic validators run automatically on every request

**Error Exposure**

- Never return a Python traceback or exception message in an HTTP response
- Log the full error server-side; return a generic message to the client


---

## Debugging Exercise

After building the API, simulate the following failure:

In `note_service.py`, introduce a bug: when updating a note, instead of updating the note in storage, write the update to a new variable that is immediately discarded.

Then:
1. Write an API test for `PUT /notes/{id}` that verifies the note was actually updated
2. Run the test — it should fail
3. Use the test failure and logging to identify what went wrong
4. Fix the bug



---

## Stretch Goals

```
Optional:
- Add pagination to GET /notes (limit + offset query parameters)
- Add a search endpoint: GET /notes?search=keyword
- Add PATCH /notes/{id} (partial update — only provided fields change)
- Add a health check endpoint: GET /health → {"status": "ok"}

Do NOT implement:
- Authentication
- A database
- Docker
- A frontend
```

---

## Definition of Done

```
[ ] All functional requirements (FR-01 through FR-08) are met
[ ] All routes return the correct HTTP status codes
[ ] Validation errors include field-level details
[ ] Error responses never expose stack traces
[ ] All API tests pass: pytest
[ ] At least 3 unit tests for the service layer pass
[ ] Logging records method, path, and status code for every request
[ ] README.md documents all endpoints with example requests and responses
[ ] No commented-out code
[ ] Feature branches used throughout
[ ] Debugging exercise completed and answers written
```

---



---

