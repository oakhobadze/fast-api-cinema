from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.cart.models import Cart, CartItem
from app.movies.models import Movie
from app.user.models import User
from decimal import Decimal
from app.order.models import Order, OrderItem, OrderStatusEnum


def get_or_create_cart(db: Session, user: User) -> Cart:
    cart = db.query(Cart).filter_by(user_id=user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def add_item_to_cart(db: Session, user: User, movie_id: int) -> CartItem:
    cart = get_or_create_cart(db, user)

    if db.query(CartItem).filter_by(cart_id=cart.id, movie_id=movie_id).first():
        raise HTTPException(status_code=400, detail="Movie already in cart")

    movie = db.query(Movie).filter_by(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    cart_item = CartItem(cart_id=cart.id, movie_id=movie_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


def remove_item_from_cart(db: Session, user: User, movie_id: int):
    cart = get_or_create_cart(db, user)
    cart_item = db.query(CartItem).filter_by(cart_id=cart.id, movie_id=movie_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    db.delete(cart_item)
    db.commit()


def get_cart(db: Session, user: User) -> Cart:
    return get_or_create_cart(db, user)


def clear_cart(db: Session, user: User):
    cart = get_or_create_cart(db, user)
    db.query(CartItem).filter_by(cart_id=cart.id).delete()
    db.commit()


def checkout_cart(db: Session, user: User):
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty.")

    total = Decimal("0.00")
    order_items = []

    for item in cart.items:
        movie = db.query(Movie).filter(Movie.id == item.movie_id).first()

        if not movie:
            raise HTTPException(status_code=404, detail=f"Movie with ID {item.movie_id} not found.")

        order_item = OrderItem(
            movie_id=movie.id,
            price_at_order=movie.price
        )
        total += Decimal(movie.price)
        order_items.append(order_item)

    new_order = Order(
        user_id=user.id,
        status=OrderStatusEnum.pending,
        total_amount=total,
        items=order_items
    )

    db.add(new_order)
    db.delete(cart)
    db.commit()
    db.refresh(new_order)
    return new_order
