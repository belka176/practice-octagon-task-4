# app/db/crud.py
from sqlalchemy.orm import Session
from app.db import models


# ---------- CRUD для Category ----------
def create_category(db: Session, title: str):
    """Создание новой категории"""
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int):
    """Получение категории по ID"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_title(db: Session, title: str):
    """Получение категории по названию"""
    return db.query(models.Category).filter(models.Category.title == title).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """Получение всех категорий"""
    return db.query(models.Category).offset(skip).limit(limit).all()


def update_category(db: Session, category_id: int, title: str):
    """Обновление категории"""
    category = get_category(db, category_id)
    if category:
        # Проверяем, не существует ли уже категория с таким названием
        existing = get_category_by_title(db, title)
        if existing and existing.id != category_id:
            return None  # или можно raise исключение
        
        category.title = title
        db.commit()
        db.refresh(category)
        return category
    return None


def delete_category(db: Session, category_id: int):
    """Удаление категории"""
    category = get_category(db, category_id)
    if category:
        # Проверяем, есть ли книги в этой категории
        books = db.query(models.Book).filter(models.Book.category_id == category_id).count()
        if books > 0:
            return False  # Нельзя удалить категорию с книгами
        db.delete(category)
        db.commit()
        return True
    return False


# ---------- CRUD для Book ----------
def create_book(db: Session, title: str, description: str, price: float, category_id: int, url: str = None):
    """Создание новой книги с проверкой существования категории"""
    # Проверяем, существует ли категория
    category = get_category(db, category_id)
    if not category:
        raise ValueError(f"Категория с ID {category_id} не существует")
    
    db_book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int):
    """Получение книги по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    """Получение всех книг"""
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_by_category(db: Session, category_id: int):
    """Получение книг по категории"""
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()


def update_book(db: Session, book_id: int, title: str = None, description: str = None, 
                price: float = None, url: str = None, category_id: int = None):
    """Обновление книги"""
    book = get_book(db, book_id)
    if book:
        if title is not None:
            book.title = title
        if description is not None:
            book.description = description
        if price is not None:
            book.price = price
        if url is not None:
            book.url = url
        if category_id is not None:
            # Проверяем, существует ли новая категория
            category = get_category(db, category_id)
            if not category:
                raise ValueError(f"Категория с ID {category_id} не существует")
            book.category_id = category_id
        db.commit()
        db.refresh(book)
        return book
    return None


def delete_book(db: Session, book_id: int):
    """Удаление книги"""
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
        return True
    return False