# app/api/books.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db import get_db
from app.db import crud
from app.schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookResponse])
def get_books(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    db: Session = Depends(get_db)
):
    """Получить список книг с возможностью фильтрации по категории"""
    if category_id:
        books = crud.get_books_by_category(db, category_id, skip=skip, limit=limit)
    else:
        books = crud.get_books(db, skip=skip, limit=limit)
    return books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по ID"""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    # Проверяем существование категории
    category = crud.get_category(db, book.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    # Исправлено: передаем Pydantic объект целиком
    return crud.create_book(db, book)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    """Обновить книгу"""
    # Если меняется категория - проверяем ее существование
    if book.category_id is not None:
        category = crud.get_category(db, book.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    # Исправлено: передаем Pydantic объект целиком
    db_book = crud.update_book(db, book_id, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу"""
    success = crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None