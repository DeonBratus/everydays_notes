from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import uuid
from datetime import datetime

from models.models import Notes
from models.models import Category
from schemas.notes_scheamas import NoteCreate, NoteUpdate

class NotesService:
    @staticmethod
    async def get_notes_list(session: AsyncSession) -> List[Notes]:
        result = await session.execute(select(Notes).where(Notes.is_archived == False))
        return result.scalars().all()

    @staticmethod
    async def create_note(session: AsyncSession, note_data: NoteCreate) -> Notes:
        if note_data.category_id is not None:
            result = await session.execute(select(Category).where(Category.id == note_data.category_id))
            category = result.scalar_one_or_none()
            if not category:
                raise ValueError("Category does not exist")
        note = Notes(
            title=note_data.title,
            content=note_data.content,
            tags=note_data.tags,
            category_id=note_data.category_id,
            is_pinned=note_data.is_pinned,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(note)
        await session.commit()
        await session.refresh(note)
        return note

    @staticmethod
    async def get_note(session: AsyncSession, note_id: uuid.UUID) -> Optional[Notes]:
        result = await session.execute(select(Notes).where(Notes.id == note_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_note(session: AsyncSession, note_id: uuid.UUID, note_data: NoteUpdate) -> Optional[Notes]:
        result = await session.execute(select(Notes).where(Notes.id == note_id))
        note = result.scalar_one_or_none()
        if not note:
            return None
        # Проверка существования категории при обновлении
        if note_data.category_id is not None:
            result = await session.execute(select(Category).where(Category.id == note_data.category_id))
            category = result.scalar_one_or_none()
            if not category:
                raise ValueError("Category does not exist")
        for field, value in note_data.dict(exclude_unset=True).items():
            setattr(note, field, value)
        note.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(note)
        return note

    @staticmethod
    async def soft_delete_note(session: AsyncSession, note_id: uuid.UUID) -> bool:
        result = await session.execute(select(Notes).where(Notes.id == note_id))
        note = result.scalar_one_or_none()
        if not note:
            return False
        note.is_archived = True
        note.updated_at = datetime.utcnow()
        await session.commit()
        return True

    @staticmethod
    async def hard_delete_note(session: AsyncSession, note_id: uuid.UUID) -> bool:
        result = await session.execute(select(Notes).where(Notes.id == note_id))
        note = result.scalar_one_or_none()
        if not note:
            return False
        await session.delete(note)
        await session.commit()
        return True
