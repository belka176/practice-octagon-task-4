import sys
import os

# Добавляем корневую папку в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal, engine, Base
from app.db import models, crud


def init_database():
    """Инициализация базы данных"""
    # Создание таблиц
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Создание категорий
        categories_data = ['Программирование', 'Художественная литература']
        created_categories = {}
        
        for cat_title in categories_data:
            # Проверяем, существует ли категория
            existing_cat = crud.get_category_by_title(db, cat_title)
            if existing_cat:
                print(f"Категория '{cat_title}' уже существует")
                created_categories[cat_title] = existing_cat
            else:
                cat = crud.create_category(db, cat_title)
                created_categories[cat_title] = cat
                print(f"Создана категория: {cat_title}")
        
        # Данные книг
        books_data = [
            # Книги по программированию
            {
                'title': 'Python для начинающих',
                'description': 'Полное руководство по Python с нуля',
                'price': 29.99,
                'category': 'Программирование',
                'url': 'https://example.com/python-beginners'
            },
            {
                'title': 'Алгоритмы и структуры данных',
                'description': 'Классический учебник по алгоритмам',
                'price': 45.50,
                'category': 'Программирование',
                'url': 'https://example.com/algorithms'
            },
            {
                'title': 'SQL для аналитиков',
                'description': 'Практическое руководство по SQL',
                'price': 34.99,
                'category': 'Программирование',
                'url': 'https://example.com/sql-analytics'
            },
            # Художественная литература
            {
                'title': 'Война и мир',
                'description': 'Роман-эпопея Льва Толстого',
                'price': 15.00,
                'category': 'Художественная литература',
                'url': 'https://example.com/war-and-peace'
            },
            {
                'title': 'Преступление и наказание',
                'description': 'Роман Фёдора Достоевского',
                'price': 12.50,
                'category': 'Художественная литература',
                'url': 'https://example.com/crime-and-punishment'
            },
            {
                'title': 'Мастер и Маргарита',
                'description': 'Роман Михаила Булгакова',
                'price': 14.99,
                'category': 'Художественная литература',
                'url': 'https://example.com/master-and-margarita'
            }
        ]
        
        # Добавление книг
        for book_data in books_data:
            category = crud.get_category_by_title(db, book_data['category'])
            if category:
                # Проверяем, есть ли уже такая книга
                existing_books = crud.get_books_by_category(db, category.id)
                book_exists = any(b.title == book_data['title'] for b in existing_books)
                
                if not book_exists:
                    book = crud.create_book(
                        db,
                        title=book_data['title'],
                        description=book_data['description'],
                        price=book_data['price'],
                        category_id=category.id,
                        url=book_data['url']
                    )
                    print(f"Добавлена книга: {book.title} (категория: {category.title})")
                else:
                    print(f"Книга '{book_data['title']}' уже существует")
            else:
                print(f"Категория '{book_data['category']}' не найдена")
        
        print("\nБаза данных успешно инициализирована!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()