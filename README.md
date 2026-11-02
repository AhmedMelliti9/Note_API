# Notes API

A shared technical notes service built with **FastAPI** and **Pydantic v2**. Designed for developer teams to capture quick technical decisions, meeting notes, snippets, and references through a predictable, consistent REST API.

---

## Features

- **CRUD Operations**: Create, read, list, update, and delete technical notes.
- **Auto-generated Metadata**: UUID identifiers, UTC creation timestamps, and automatic `updated_at` tracking.
- **Layered Architecture**: Strict separation of concerns between HTTP routes, Pydantic contracts, business logic services, and in-memory storage.
- **Strict Server-Side Validation**: Field length limits and whitespace sanitization.
- **Standardized Error Handling**: Uniform JSON error formats across business, validation, client, and internal exceptions without leaking stack traces.
- **Structured Request Logging**: Non-intrusive logging of HTTP method, route, and status code (request bodies are never logged for security).
- **Interactive Documentation**: Auto-generated OpenAPI (Swagger UI) and ReDoc.

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ (Tested on Python 3.14) |
| Web Framework | FastAPI |
| Validation | Pydantic v2 |
| ASGI Server | Uvicorn |
| Storage | Pure Python in-memory store (dictionary-based) |
| Testing | pytest + httpx |

---

## Project Structure

```
Note_API/
├── README.md                  # Project documentation & guides
├── requirements.txt           # Frozen project dependencies
├── pytest.ini                 # Pytest configuration
├── .gitignore                 # Python, venv, and environment ignores
└── app/
    ├── __init__.py
    ├── main.py                # FastAPI application entrypoint & middleware
    ├── logging_config.py      # Structured logging setup
    ├── exceptions.py          # Custom domain exceptions (NoteNotFoundError)
    ├── handlers.py            # Centralized exception & error response handlers
    ├── models/
    │   ├── __init__.py
    │   ├── error.py           # Standard ErrorResponse schema
    │   └── note.py            # NoteCreate, NoteUpdate, NoteResponse schemas
    ├── routes/
    │   ├── __init__.py
    │   └── notes.py           # Notes API endpoints (CRUD routes)
    ├── services/
    │   ├── __init__.py
    │   └── note_service.py    # Business logic layer
    ├── storage/
    │   ├── __init__.py
    │   └── in_memory.py       # In-memory dictionary data store
    └── tests/
        ├── __init__.py
        ├── conftest.py        # Pytest fixtures and state isolation
        ├── test_note_service.py # Unit tests for business logic
        └── test_notes.py      # API integration tests
```

---

## Getting Started

### 1. Prerequisites

- Python 3.11 or higher installed on your system.

### 2. Setup Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Development Server

```bash
uvicorn app.main:app --reload
```

The service will start at `http://127.0.0.1:8000`.

### 5. Interactive API Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## API Endpoints

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| `POST` | `/notes` | Create a new note | `201 Created` |
| `GET` | `/notes` | Retrieve all notes | `200 OK` |
| `GET` | `/notes/{id}` | Retrieve a note by ID | `200 OK` |
| `PUT` | `/notes/{id}` | Replace/update an existing note | `200 OK` |
| `DELETE` | `/notes/{id}` | Delete a note by ID | `204 No Content` |

---

## Request & Response Examples

### 1. Create a Note (`POST /notes`)

**Request:**
```http
POST /notes HTTP/1.1
Content-Type: application/json

{
  "title": "Architecture Decision: In-Memory Store",
  "content": "Storing notes in-memory for Project 03 to isolate the HTTP layer."
}
```

**Response (`201 Created`):**
```json
{
  "id": "e9ef8025-355c-40fa-8847-066c4e383e4f",
  "title": "Architecture Decision: In-Memory Store",
  "content": "Storing notes in-memory for Project 03 to isolate the HTTP layer.",
  "created_at": "2026-11-02T20:55:50.991933",
  "updated_at": "2026-11-02T20:55:50.991933"
}
```

---

### 2. Retrieve All Notes (`GET /notes`)

**Request:**
```http
GET /notes HTTP/1.1
```

**Response (`200 OK`):**
```json
[
  {
    "id": "e9ef8025-355c-40fa-8847-066c4e383e4f",
    "title": "Architecture Decision: In-Memory Store",
    "content": "Storing notes in-memory for Project 03 to isolate the HTTP layer.",
    "created_at": "2026-11-02T20:55:50.991933",
    "updated_at": "2026-11-02T20:55:50.991933"
  }
]
```

---

### 3. Retrieve a Single Note (`GET /notes/{id}`)

**Request:**
```http
GET /notes/e9ef8025-355c-40fa-8847-066c4e383e4f HTTP/1.1
```

**Response (`200 OK`):**
```json
{
  "id": "e9ef8025-355c-40fa-8847-066c4e383e4f",
  "title": "Architecture Decision: In-Memory Store",
  "content": "Storing notes in-memory for Project 03 to isolate the HTTP layer.",
  "created_at": "2026-11-02T20:55:50.991933",
  "updated_at": "2026-11-02T20:55:50.991933"
}
```

---

### 4. Update a Note (`PUT /notes/{id}`)

**Request:**
```http
PUT /notes/e9ef8025-355c-40fa-8847-066c4e383e4f HTTP/1.1
Content-Type: application/json

{
  "title": "Updated Architecture Decision",
  "content": "Updated content with additional context."
}
```

**Response (`200 OK`):**
```json
{
  "id": "e9ef8025-355c-40fa-8847-066c4e383e4f",
  "title": "Updated Architecture Decision",
  "content": "Updated content with additional context.",
  "created_at": "2026-11-02T20:55:50.991933",
  "updated_at": "2026-11-02T21:10:14.312926"
}
```

---

### 5. Delete a Note (`DELETE /notes/{id}`)

**Request:**
```http
DELETE /notes/e9ef8025-355c-40fa-8847-066c4e383e4f HTTP/1.1
```

**Response (`204 No Content`):**
*(Empty body)*

---

## Validation & Error Handling Rules

### Validation Constraints

| Field | Required in Create | Length Constraints | Sanitization |
|---|---|---|---|
| `title` | Yes | 3 to 200 characters | Leading and trailing whitespace stripped |
| `content` | Yes | 1 to 10,000 characters | Leading and trailing whitespace stripped |

In `NoteUpdate`, both fields are optional, but if provided, they undergo identical length and whitespace validation.

---

### Standard Error Response Format

All error responses adhere to a consistent JSON structure:

#### Resource Not Found (`404 Not Found`)
```json
{
  "error": "note_not_found",
  "message": "Note with id 'invalid-id' does not exist",
  "field": null
}
```

#### Validation Error (`422 Unprocessable Content`)
```json
{
  "error": "validation_error",
  "message": "Invalid input",
  "field": "title",
  "detail": "String should have at least 3 characters"
}
```

#### Malformed JSON (`400 Bad Request`)
```json
{
  "error": "bad_request",
  "message": "Malformed JSON body",
  "field": null
}
```

#### Internal Server Error (`500 Internal Server Error`)
```json
{
  "error": "internal_server_error",
  "message": "Internal server error",
  "field": null
}
```
*(Internal tracebacks are logged server-side and never exposed to the client).*

---

## Testing

The test suite includes both **unit tests** for the service layer and **HTTP integration tests** using FastAPI's `TestClient`.

### Running Tests

```bash
pytest
```

or with verbose reporting:

```bash
pytest --tb=short -v
```

### Test Coverage Summary

- **Unit Tests (`test_note_service.py`)**:
  - `test_create_note_generates_id_and_timestamps`: Verifies UUID and timestamps are populated.
  - `test_get_non_existent_note_raises_exception`: Verifies `NoteNotFoundError` is raised when missing.
  - `test_update_note_updates_updated_at_not_created_at`: Verifies timestamp preservation.
- **Integration Tests (`test_notes.py`)**:
  - Valid POST, empty title (422), title too short/long (422), content too long (422), whitespace stripping.
  - Missing content (422).
  - List empty notes and populated notes (200).
  - Get note by ID (200) and missing ID (404).
  - Put note updates (200), validation failures (422), non-existent (404).
  - Delete note (204) and repeated/missing delete (404).

---

## Debugging Exercise

### Simulated Bug
In `app/services/note_service.py`, simulated a failure where the updated note is assigned to a local variable that is immediately discarded rather than stored:

```python
# Discarded update bug
updated_note = note.copy()
updated_note["title"] = data.title
# Note store was never mutated
```

### Observation & Resolution
1. **Test Failure**: Running `test_put_note_valid_data` failed because the subsequent `GET /notes/{id}` returned the original un-mutated values.
2. **Logging Analysis**: Request logging showed `PUT /notes/{id} 200`, but subsequent reads indicated state was unchanged.
3. **Fix**: Ensured `self._store.update(...)` directly mutates the persistent dictionary store in-memory and returns the updated reference.
