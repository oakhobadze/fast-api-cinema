from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.user.dependencies import get_current_user
from app.order import services
from app.order.schemas import OrderRead

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderRead])
def get_user_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return services.get_orders_for_user(db, user)


@router.get("/{order_id}", response_model=OrderRead)
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return services.get_order_by_id(db, user, order_id)


@router.delete("/{order_id}", response_model=OrderRead)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return services.cancel_order(db, user, order_id)
