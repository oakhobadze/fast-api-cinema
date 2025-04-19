import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.user.email_utils import send_reset_password_email
from app.user.models import User, ActivationToken, UserGroup
from app.user.schemas import UserCreate
from app.user.email_utils import send_activation_email
from jose import jwt

from app.core.config import SECRET_KEY, ALGORITHM
from app.user.schemas import UserLogin



def create_user(db: Session, user_data: UserCreate):
    if db.query(User).filter(User.email == user_data.email).first():
        raise ValueError("Email already registered")

    group = db.query(UserGroup).filter(UserGroup.name == "USER").first()
    if not group:
        group = UserGroup(name="USER")
        db.add(group)
        db.commit()
        db.refresh(group)

    hashed_password = bcrypt.hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=False,
        group_id=group.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(hours=24)

    activation = ActivationToken(user_id=user.id, token=token, expires_at=expires)
    db.add(activation)
    db.commit()

    send_activation_email(user.email, token)

    return user

def activate_user_account(db: Session, token: str):
    activation_token = db.query(ActivationToken).filter(ActivationToken.token == token).first()

    if not activation_token:
        raise ValueError("Invalid activation token")

    if activation_token.expires_at < datetime.utcnow():
        db.delete(activation_token)
        db.commit()
        raise ValueError("Activation token has expired")

    user = db.query(User).filter(User.id == activation_token.user_id).first()
    if not user:
        raise ValueError("User not found")

    if user.is_active:
        return {"message": "Account is already activated."}

    user.is_active = True
    db.delete(activation_token)
    db.commit()

    return {"message": "Account activated successfully!"}

def authenticate_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise ValueError("Invalid credentials")
    if not user.is_active:
        raise ValueError("User is not activated")
    if not bcrypt.verify(login_data.password, user.hashed_password):
        raise ValueError("Invalid credentials")
    return user

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def change_password_with_current(db: Session, user: User, current_password: str, new_password: str):
    if not bcrypt.verify(current_password, user.hashed_password):
        raise ValueError("Current password is incorrect")

    user.hashed_password = bcrypt.hash(new_password)
    db.commit()
    return {"message": "Password changed successfully!"}

def reset_password_request(db: Session, email: str, new_password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("Email not registered")

    token = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(hours=1)

    db.query(ActivationToken).filter(ActivationToken.user_id == user.id).delete()

    db.add(ActivationToken(user_id=user.id, token=token, expires_at=expires))
    db.commit()

    send_reset_password_email(user.email, token, new_password)

    return {"message": "Password reset link has been sent!"}

def reset_password(db: Session, token: str, new_password: str):
    reset_token = db.query(ActivationToken).filter(ActivationToken.token == token).first()

    if not reset_token:
        raise ValueError("Invalid reset token")

    if reset_token.expires_at < datetime.utcnow():
        db.delete(reset_token)
        db.commit()
        raise ValueError("Reset token has expired")

    user = db.query(User).filter(User.id == reset_token.user_id).first()
    if not user:
        raise ValueError("User not found")

    user.hashed_password = bcrypt.hash(new_password)
    db.delete(reset_token)
    db.commit()

    return {"message": "Password has been reset successfully!"}
