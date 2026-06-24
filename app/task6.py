from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import books, categories
from app.db.db import engine
from app.db.models import Base

# Создаем таблицы если их нет
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book API",
    description="API для управления книгами и категориями",
    version="1.0.0"
)

# Настройка CORS (для Postman и фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(books.router)
app.include_router(categories.router)


@app.get("/health")
def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok", "message": "Service is running"}


@app.get("/")
def root():
    return {
        "message": "Welcome to Book API",
        "docs": "/docs",
        "health": "/health"
    }