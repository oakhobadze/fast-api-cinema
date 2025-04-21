from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.user.dependencies import get_current_user
from app.order import services
from app.order.schemas import OrderRead

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get(
    "/",
    response_model=List[OrderRead],
    summary="Get user's orders",
    description="Returns a list of all orders made by the currently authenticated user."
)
def get_user_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Retrieve all orders made by the current authenticated user.
    """
    return services.get_orders_for_user(db, user)


@router.get(
    "/{order_id}",
    response_model=OrderRead,
    summary="Get order details",
    description="Returns detailed information about a specific order belonging to the current user."
)
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Retrieve detailed information about a specific order by ID.
    """
    return services.get_order_by_id(db, user, order_id)


@router.delete(
    "/{order_id}",
    response_model=OrderRead,
    summary="Cancel an order",
    description="Cancels a specific order if it belongs to the current user and is eligible for cancellation."
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Cancel an order by ID if it belongs to the current authenticated user.
    """
    return services.cancel_order(db, user, order_id)
