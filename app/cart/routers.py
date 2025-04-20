from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.cart import schemas, services
from app.core.database import get_db
from app.user.dependencies import get_current_user
from app.user.models import User

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/items/", response_model=schemas.CartItemRead)
def add_item_to_cart(
    item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.add_item_to_cart(db, current_user, item.movie_id)

@router.delete("/items/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_cart(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    services.remove_item_from_cart(db, current_user, movie_id)
    return

@router.get("/", response_model=schemas.CartRead)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_cart(db, current_user)

@router.post("/checkout", status_code=status.HTTP_200_OK)
def checkout_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    services.checkout_cart(db, current_user)
    return {"message": "Purchase successful"}

@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    services.clear_cart(db, current_user)
    return
