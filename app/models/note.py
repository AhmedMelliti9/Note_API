"""Pydantic models for the Notes API.

- NoteCreate: what a client sends to create a note (validated title + content).
- NoteUpdate: what a client sends to update a note (both fields optional).
- NoteResponse: what the API returns to the client (includes id, created_at, updated_at).
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class NoteCreate(BaseModel):
    """Schema for creating a new note.

    Validation rules:
    - Title: required, 3-200 characters, strip whitespace.
    - Content: required, 1-10,000 characters, strip whitespace.
    """

    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=1, max_length=10000)

    @field_validator("title", mode="before")
    @classmethod
    def strip_title(cls, v: object) -> object:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("content", mode="before")
    @classmethod
    def strip_content(cls, v: object) -> object:
        if isinstance(v, str):
            return v.strip()
        return v


class NoteUpdate(BaseModel):
    """Schema for updating an existing note.

    Validation rules:
    - Title: optional, 3-200 characters, strip whitespace.
    - Content: optional, 1-10,000 characters, strip whitespace.
    """

    title: Optional[str] = Field(None, min_length=3, max_length=200)
    content: Optional[str] = Field(None, min_length=1, max_length=10000)

    @field_validator("title", mode="before")
    @classmethod
    def strip_title(cls, v: object) -> object:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("content", mode="before")
    @classmethod
    def strip_content(cls, v: object) -> object:
        if isinstance(v, str):
            return v.strip()
        return v


class NoteResponse(BaseModel):
    """Schema returned to the client for any note.

    Includes the server-generated fields: id, created_at, updated_at.
    """

    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
