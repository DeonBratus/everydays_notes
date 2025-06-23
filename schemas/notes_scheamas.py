from pydantic import BaseModel
from typing import Optional
import uuid

class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None
    tags: Optional[list] = None
    category_id: Optional[uuid.UUID] = None
    is_pinned: Optional[bool] = False

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[list] = None
    category_id: Optional[uuid.UUID] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
