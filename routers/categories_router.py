from fastapi import APIRouter, Depends, HTTPException
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from services.categories_service import CategoriesService, CategoryCreate, CategoryUpdate
from database.db import get_db

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("/")
async def get_categories_list(session: AsyncSession = Depends(get_db)):
    return await CategoriesService.get_categories_list(session)


@router.post("/create")
async def create_category(category: CategoryCreate, session: AsyncSession = Depends(get_db)):
    return await CategoriesService.create_category(session, category)


@router.get("/{id}")
async def get_category(id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    category = await CategoriesService.get_category(session, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/{id}/update")
async def update_category(id: uuid.UUID, category: CategoryUpdate, session: AsyncSession = Depends(get_db)):
    updated = await CategoriesService.update_category(session, id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated


@router.delete("/{id}/soft_delete")
async def soft_delete_category(id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    result = await CategoriesService.soft_delete_category(session, id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"success": True}


@router.delete("/{id}/hard_delete")
async def hard_delete_category(id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    result = await CategoriesService.hard_delete_category(session, id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"success": True}