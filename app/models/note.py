"""Pydantic models for the Notes API.

- NoteCreate: what a client sends to create a note (title + content only).
- NoteUpdate: what a client sends to update a note (both fields optional).
- NoteResponse: what the API returns to the client (includes id, created_at, updated_at).
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NoteCreate(BaseModel):
    """Schema for creating a new note.

    Both title and content are required — a note without either
    is meaningless.
    """

    title: str
    content: str


class NoteUpdate(BaseModel):
    """Schema for updating an existing note.

    Both fields are optional so the client can update only the
    fields it wants to change (partial update via PUT).
    """

    title: Optional[str] = None
    content: Optional[str] = None


class NoteResponse(BaseModel):
    """Schema returned to the client for any note.

    Includes the server-generated fields: id, created_at, updated_at.
    """

    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
