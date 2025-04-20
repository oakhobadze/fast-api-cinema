from pydantic import BaseModel
from datetime import datetime
from app.movies.schemas import MovieBase

class CartItemBase(BaseModel):
    movie_id: int

class CartItemCreate(CartItemBase):
    pass

class CartItemRead(BaseModel):
    id: int
    added_at: datetime
    movie: MovieBase

    class Config:
        orm_mode = True

class CartRead(BaseModel):
    id: int
    items: list[CartItemRead]

    class Config:
        orm_mode = True
