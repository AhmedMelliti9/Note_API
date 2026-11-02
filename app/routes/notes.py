"""Notes CRUD routes.

POST   /notes          → create a note (201)
GET    /notes          → list all notes (200)
GET    /notes/{id}     → get one note (200) or 404
PUT    /notes/{id}     → replace a note (200) or 404
DELETE /notes/{id}     → delete a note (204) or 404
"""

from fastapi import APIRouter, Response, status

from app.models.note import NoteCreate, NoteResponse, NoteUpdate
from app.services.note_service import NoteService
from app.storage.in_memory import NoteStore

router = APIRouter()

# Shared service instance
_store = NoteStore()
_service = NoteService(_store)


@router.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(data: NoteCreate):
    """Create a new note."""
    return _service.create_note(data)


@router.get("/notes", response_model=list[NoteResponse], status_code=status.HTTP_200_OK)
def list_notes():
    """Retrieve all notes."""
    return _service.get_all_notes()


@router.get("/notes/{note_id}", response_model=NoteResponse, status_code=status.HTTP_200_OK)
def get_note(note_id: str):
    """Retrieve a single note by its ID."""
    return _service.get_note(note_id)


@router.put("/notes/{note_id}", response_model=NoteResponse, status_code=status.HTTP_200_OK)
def update_note(note_id: str, data: NoteUpdate):
    """Replace/update an existing note."""
    return _service.update_note(note_id, data)


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str):
    """Delete a note by its ID."""
    _service.delete_note(note_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
