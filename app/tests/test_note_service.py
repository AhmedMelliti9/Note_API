"""Unit tests for the NoteService layer without HTTP."""

import time
import pytest

from app.exceptions import NoteNotFoundError
from app.models.note import NoteCreate, NoteUpdate
from app.services.note_service import NoteService
from app.storage.in_memory import NoteStore


def test_create_note_generates_id_and_timestamps():
    """Test that creating a note generates an ID and timestamps."""
    store = NoteStore()
    service = NoteService(store)

    data = NoteCreate(title="Test Title", content="Test Content")
    created = service.create_note(data)

    assert created.id is not None
    assert len(created.id) > 0
    assert created.title == "Test Title"
    assert created.content == "Test Content"
    assert created.created_at is not None
    assert created.updated_at is not None
    assert created.created_at == created.updated_at


def test_get_non_existent_note_raises_exception():
    """Test that getting a non-existent note raises NoteNotFoundError."""
    store = NoteStore()
    service = NoteService(store)

    with pytest.raises(NoteNotFoundError) as exc_info:
        service.get_note("non-existent-id-12345")

    assert "non-existent-id-12345" in str(exc_info.value)
    assert exc_info.value.note_id == "non-existent-id-12345"


def test_update_note_updates_updated_at_not_created_at():
    """Test that updating a note updates updated_at but not created_at."""
    store = NoteStore()
    service = NoteService(store)

    created = service.create_note(NoteCreate(title="Original", content="Original Content"))
    original_created_at = created.created_at
    original_updated_at = created.updated_at

    # Ensure a small timestamp advance
    time.sleep(0.01)

    updated = service.update_note(created.id, NoteUpdate(title="Modified"))

    assert updated.title == "Modified"
    assert updated.content == "Original Content"
    assert updated.created_at == original_created_at
    assert updated.updated_at > original_updated_at
