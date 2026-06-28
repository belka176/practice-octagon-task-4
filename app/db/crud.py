# app/db/crud.py
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import CategoryCreate, CategoryUpdate, BookCreate, BookUpdate


# ---------- CRUD для Category ----------
def create_category(db: Session, category: CategoryCreate):
    """Создание новой категории"""
    db_category = models.Category(title=category.title)
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


def update_category(db: Session, category_id: int, category: CategoryUpdate):
    """Обновление категории"""
    db_category = get_category(db, category_id)
    if db_category:
        if category.title is not None:
            # Проверяем, не существует ли уже категория с таким названием
            existing = get_category_by_title(db, category.title)
            if existing and existing.id != category_id:
                return None
            
            db_category.title = category.title
            db.commit()
            db.refresh(db_category)
        return db_category
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
def create_book(db: Session, book: BookCreate):
    """Создание новой книги с проверкой существования категории"""
    # Проверяем, существует ли категория
    category = get_category(db, book.category_id)
    if not category:
        raise ValueError(f"Категория с ID {book.category_id} не существует")
    
    db_book = models.Book(
        title=book.title,
        description=book.description,
        price=book.price,
        url=book.url,
        category_id=book.category_id
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


def get_books_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    """Получение книг по категории"""
    return db.query(models.Book).filter(models.Book.category_id == category_id).offset(skip).limit(limit).all()


def update_book(db: Session, book_id: int, book: BookUpdate):
    """Обновление книги"""
    db_book = get_book(db, book_id)
    if db_book:
        if book.title is not None:
            db_book.title = book.title
        if book.description is not None:
            db_book.description = book.description
        if book.price is not None:
            db_book.price = book.price
        if book.url is not None:
            db_book.url = book.url
        if book.category_id is not None:
            # Проверяем, существует ли новая категория
            category = get_category(db, book.category_id)
            if not category:
                raise ValueError(f"Категория с ID {book.category_id} не существует")
            db_book.category_id = book.category_id
        db.commit()
        db.refresh(db_book)
        return db_book
    return None


def delete_book(db: Session, book_id: int):
    """Удаление книги"""
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
        return True
    return False