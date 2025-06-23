from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import uuid

from models.models import Category
from schemas.categories_schemas import CategoryCreate, CategoryUpdate

class CategoriesService:
    @staticmethod
    async def get_categories_list(session: AsyncSession) -> List[Category]:
        result = await session.execute(select(Category))
        return result.scalars().all()

    @staticmethod
    async def create_category(session: AsyncSession, category_data: CategoryCreate) -> Category:
        category = Category(
            name=category_data.name,
            color=category_data.color,
        )
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category

    @staticmethod
    async def get_category(session: AsyncSession, category_id: uuid.UUID) -> Optional[Category]:
        result = await session.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_category(session: AsyncSession, category_id: uuid.UUID, category_data: CategoryUpdate) -> Optional[Category]:
        result = await session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if not category:
            return None
        for field, value in category_data.dict(exclude_unset=True).items():
            setattr(category, field, value)
        await session.commit()
        await session.refresh(category)
        return category

    @staticmethod
    async def soft_delete_category(session: AsyncSession, category_id: uuid.UUID) -> bool:
        result = await session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if not category:
            return False
        category.name = f"_deleted_{category.id}"
        await session.commit()
        return True

    @staticmethod
    async def hard_delete_category(session: AsyncSession, category_id: uuid.UUID) -> bool:
        result = await session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if not category:
            return False
        await session.delete(category)
        await session.commit()
        return True