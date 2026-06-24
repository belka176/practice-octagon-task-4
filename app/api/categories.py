# app/api/categories.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.db import get_db
from app.db import crud
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех категорий"""
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию"""
    return crud.create_category(db, category)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    """Обновить категорию"""
    db_category = crud.update_category(db, category_id, category)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию"""
    success = crud.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return None