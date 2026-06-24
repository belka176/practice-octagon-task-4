import sys
import os

# Добавляем корневую папку в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db import crud


def main():
    """Основная функция для вывода данных"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("СПИСОК КАТЕГОРИЙ И КНИГ")
        print("=" * 60)
        
        # Получаем все категории
        categories = crud.get_categories(db)
        
        for category in categories:
            print(f"\n Категория: {category.title} (ID: {category.id})")
            print("-" * 50)
            
            # Получаем книги для этой категории
            books = crud.get_books_by_category(db, category.id)
            
            if books:
                for book in books:
                    print(f"  {book.title}")
                    print(f"     Описание: {book.description}")
                    print(f"     Цена: {book.price:.2f} руб.")
                    if book.url:
                        print(f"     Ссылка: {book.url}")
                    print()
            else:
                print("  Нет книг в этой категории")
        
        print("=" * 60)
        
        # Вывод статистики
        all_books = crud.get_books(db)
        print(f"\n Всего книг в базе: {len(all_books)}")
        print(f"Всего категорий: {len(categories)}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()