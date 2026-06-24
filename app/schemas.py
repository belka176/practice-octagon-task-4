# app/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional

# ----- Схемы для Category -----
class CategoryBase(BaseModel):
    title: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    title: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ----- Схемы для Book -----
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    url: Optional[str] = None
    category_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    category_id: Optional[int] = None

class BookResponse(BookBase):
    id: int
    category: Optional[CategoryResponse] = None
    
    model_config = ConfigDict(from_attributes=True)