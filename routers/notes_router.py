from fastapi import APIRouter, Depends, HTTPException
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from services.notes_service import NotesService, NoteCreate, NoteUpdate
from database.db import get_db

router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.get("/")
async def get_notes_list(session: AsyncSession = Depends(get_db)):
    return await NotesService.get_notes_list(session)


@router.post("/create")
async def create_notes(note: NoteCreate, session: AsyncSession = Depends(get_db)):
    try:
        return await NotesService.create_note(session, note)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}")
async def get_note(id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    note = await NotesService.get_note(session, id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.patch("/{id}/update")
async def update_note(id: uuid.UUID, note: NoteUpdate, session: AsyncSession = Depends(get_db)):
    try:
        updated = await NotesService.update_note(session, id, note)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


@router.delete("/{id}/soft_delete")
async def soft_delete_note(id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    result = await NotesService.soft_delete_note(session, id)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"success": True}


@router.delete("/{id}/hard_delete")
async def hard_delete_note(id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    result = await NotesService.hard_delete_note(session, id)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"success": True}