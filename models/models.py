import uuid
from sqlalchemy import Integer, String, Column, UUID, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import Base

class Notes(Base):
    __tablename__ = "notes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_pinned = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    tags = Column(JSON, default=list, nullable=True)
    category_id = Column(UUID(as_uuid=True), nullable=True)

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), nullable=False)
    color = Column(String(64), nullable=True)




