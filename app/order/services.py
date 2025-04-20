from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.order.models import Order, OrderStatusEnum
from app.cart.models import Cart, CartItem
from app.user.models import User


def get_orders_for_user(db: Session, user: User):
    return db.query(Order).filter(Order.user_id == user.id).order_by(Order.created_at.desc()).all()


def get_order_by_id(db: Session, user: User, order_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def cancel_order(db: Session, user: User, order_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != OrderStatusEnum.pending:
        raise HTTPException(status_code=400, detail="Only pending orders can be canceled")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.flush()

    for item in order.items:
        exists = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.movie_id == item.movie_id
        ).first()
        if not exists:
            cart_item = CartItem(cart_id=cart.id, movie_id=item.movie_id)
            db.add(cart_item)

    order.status = OrderStatusEnum.canceled
    db.commit()
    db.refresh(order)
    return order
