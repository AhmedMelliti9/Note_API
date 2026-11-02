"""API integration tests for Notes CRUD endpoints."""


def test_post_note_valid_data(client):
    """POST /notes with valid data -> 201 + note in response."""
    payload = {"title": "Team Meeting", "content": "Discuss Q1 roadmap and architecture."}
    response = client.post("/notes", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_post_note_empty_title(client):
    """POST /notes with empty title -> 422 + validation error in response."""
    payload = {"title": "", "content": "Valid content"}
    response = client.post("/notes", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["field"] == "title"
    assert "detail" in data


def test_post_note_title_too_short(client):
    """POST /notes with title < 3 chars -> 422."""
    response = client.post("/notes", json={"title": "ab", "content": "Valid content"})
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["field"] == "title"


def test_post_note_title_too_long(client):
    """POST /notes with title > 200 chars -> 422."""
    long_title = "a" * 201
    response = client.post("/notes", json={"title": long_title, "content": "Valid content"})
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["field"] == "title"


def test_post_note_content_too_long(client):
    """POST /notes with content > 10,000 chars -> 422."""
    long_content = "c" * 10001
    response = client.post("/notes", json={"title": "Valid Title", "content": long_content})
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["field"] == "content"


def test_post_note_strips_whitespace(client):
    """POST /notes strips leading and trailing whitespace from title and content."""
    payload = {"title": "   Spaced Title   ", "content": "   Spaced Content   "}
    response = client.post("/notes", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Spaced Title"
    assert data["content"] == "Spaced Content"


def test_post_note_missing_content(client):
    """POST /notes with missing content -> 422 + validation error in response."""
    payload = {"title": "Valid Title"}
    response = client.post("/notes", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["field"] == "content"
    assert "detail" in data


def test_get_notes_empty(client):
    """GET /notes with no notes -> 200 + empty list."""
    response = client.get("/notes")

    assert response.status_code == 200
    assert response.json() == []


def test_get_notes_with_data(client):
    """GET /notes with notes -> 200 + list of notes."""
    client.post("/notes", json={"title": "Note 1", "content": "Content 1"})
    client.post("/notes", json={"title": "Note 2", "content": "Content 2"})

    response = client.get("/notes")

    assert response.status_code == 200
    notes = response.json()
    assert len(notes) == 2
    assert notes[0]["title"] == "Note 1"
    assert notes[1]["title"] == "Note 2"


def test_get_note_by_valid_id(client):
    """GET /notes/{id} with valid id -> 200 + note."""
    created = client.post("/notes", json={"title": "Unique Note", "content": "Unique Content"}).json()
    note_id = created["id"]

    response = client.get(f"/notes/{note_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Unique Note"
    assert data["content"] == "Unique Content"


def test_get_note_by_invalid_id(client):
    """GET /notes/{id} with invalid id -> 404 + error."""
    response = client.get("/notes/non-existent-id")

    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "note_not_found"
    assert "non-existent-id" in data["message"]
    assert data["field"] is None


def test_put_note_valid_data(client):
    """PUT /notes/{id} with valid data -> 200 + updated note."""
    created = client.post("/notes", json={"title": "Original Title", "content": "Original Content"}).json()
    note_id = created["id"]

    update_payload = {"title": "Updated Title", "content": "Updated Content"}
    response = client.put(f"/notes/{note_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content"
    assert data["created_at"] == created["created_at"]


def test_put_note_validation_error(client):
    """PUT /notes/{id} with invalid title length -> 422."""
    created = client.post("/notes", json={"title": "Valid Title", "content": "Valid Content"}).json()
    note_id = created["id"]

    response = client.put(f"/notes/{note_id}", json={"title": "no"})
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["field"] == "title"


def test_put_note_non_existent_id(client):
    """PUT /notes/{id} with non-existent id -> 404 + error."""
    response = client.put("/notes/missing-id", json={"title": "New Title"})

    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "note_not_found"
    assert "missing-id" in data["message"]
    assert data["field"] is None


def test_delete_note_valid_id(client):
    """DELETE /notes/{id} with valid id -> 204."""
    created = client.post("/notes", json={"title": "To Delete", "content": "Delete me"}).json()
    note_id = created["id"]

    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 204
    assert response.text == ""

    # Verify note is gone
    get_res = client.get(f"/notes/{note_id}")
    assert get_res.status_code == 404


def test_delete_note_non_existent_id(client):
    """DELETE /notes/{id} with non-existent id -> 404 + error."""
    response = client.delete("/notes/missing-id")

    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "note_not_found"
    assert "missing-id" in data["message"]
    assert data["field"] is None
