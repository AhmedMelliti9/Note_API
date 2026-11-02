"""Custom exception classes for the Notes API."""


class NoteNotFoundError(Exception):
    """Raised when a requested note does not exist."""

    def __init__(self, note_id: str):
        self.note_id = note_id
        super().__init__(f"Note with id '{note_id}' does not exist")
