from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.user import schemas, services
from app.user.schemas import Token, UserLogin
from app.user.services import authenticate_user, create_access_token
from app.user.dependencies import get_current_user
from app.user.models import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserRead)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return services.create_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/activate/{token}")
def activate_account(token: str, db: Session = Depends(get_db)):
    try:
        return services.activate_user_account(db, token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, user_data)
        access_token = create_access_token(data={"sub": str(user.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=schemas.UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/change-password")
def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return services.change_password_with_current(db, current_user, current_password, new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password-request")
def reset_password_request(email: str, new_password: str, db: Session = Depends(get_db)):
    try:
        return services.reset_password_request(db, email, new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reset-password/{token}")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    try:
        return services.reset_password(db, token, new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
