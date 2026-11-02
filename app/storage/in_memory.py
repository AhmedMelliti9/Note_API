"""In-memory data store for notes.

This module has no knowledge of FastAPI or HTTP — it is just a data store.
It can later be replaced with a real database without affecting the rest
of the application.
"""

import uuid
from datetime import datetime


class NoteStore:
    """Stores notes in a dict keyed by ID.

    Supports: create, get by ID, get all, update, delete.
    """

    def __init__(self):
        self._notes: dict[str, dict] = {}

    def create(self, title: str, content: str) -> dict:
        """Create a new note with a generated UUID and timestamps."""
        note_id = str(uuid.uuid4())
        now = datetime.utcnow()
        note = {
            "id": note_id,
            "title": title,
            "content": content,
            "created_at": now,
            "updated_at": now,
        }
        self._notes[note_id] = note
        return note

    def get(self, note_id: str) -> dict | None:
        """Return a note by ID, or None if it does not exist."""
        return self._notes.get(note_id)

    def get_all(self) -> list[dict]:
        """Return all notes as a list."""
        return list(self._notes.values())

    def update(self, note_id: str, title: str | None = None, content: str | None = None) -> dict | None:
        """Update only the provided fields of an existing note.

        Refreshes updated_at. Returns the updated note, or None if
        the note does not exist.
        """
        note = self._notes.get(note_id)
        if note is None:
            return None

        if title is not None:
            note["title"] = title
        if content is not None:
            note["content"] = content
        note["updated_at"] = datetime.utcnow()

        return note

    def delete(self, note_id: str) -> bool:
        """Remove a note by ID. Return True if it existed, False otherwise."""
        if note_id in self._notes:
            del self._notes[note_id]
            return True
        return False
