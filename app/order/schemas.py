from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import List
from app.movies.schemas import MovieBase


class OrderItemRead(BaseModel):
    id: int
    price_at_order: Decimal
    movie: MovieBase

    class Config:
        orm_mode = True


class OrderRead(BaseModel):
    id: int
    status: str
    created_at: datetime
    total_amount: Decimal
    items: List[OrderItemRead]

    class Config:
        orm_mode = True
