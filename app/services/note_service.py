"""Service layer for note operations.

This module contains business logic only. It delegates data access to
the storage layer and raises Python exceptions when things go wrong.
It does NOT import FastAPI directly.
"""

from app.exceptions import NoteNotFoundError
from app.models.note import NoteCreate, NoteUpdate, NoteResponse
from app.storage.in_memory import NoteStore


class NoteService:
    """Handles note business logic, backed by an in-memory store."""

    def __init__(self, store: NoteStore):
        self._store = store

    def create_note(self, data: NoteCreate) -> NoteResponse:
        """Create a new note and return its response representation."""
        note = self._store.create(title=data.title, content=data.content)
        return NoteResponse(**note)

    def get_note(self, note_id: str) -> NoteResponse:
        """Get a single note by ID. Raises NoteNotFoundError if missing."""
        note = self._store.get(note_id)
        if note is None:
            raise NoteNotFoundError(note_id)
        return NoteResponse(**note)

    def get_all_notes(self) -> list[NoteResponse]:
        """Return all notes."""
        return [NoteResponse(**note) for note in self._store.get_all()]

    def update_note(self, note_id: str, data: NoteUpdate) -> NoteResponse:
        """Update an existing note. Raises NoteNotFoundError if missing."""
        note = self._store.update(
            note_id,
            title=data.title,
            content=data.content,
        )
        if note is None:
            raise NoteNotFoundError(note_id)
        return NoteResponse(**note)

    def delete_note(self, note_id: str) -> None:
        """Delete a note by ID. Raises NoteNotFoundError if missing."""
        deleted = self._store.delete(note_id)
        if not deleted:
            raise NoteNotFoundError(note_id)
