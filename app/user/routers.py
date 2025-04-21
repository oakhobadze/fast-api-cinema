from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.user import schemas, services
from app.user.schemas import Token, UserLogin
from app.user.services import authenticate_user, create_access_token
from app.user.dependencies import get_current_user
from app.user.models import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
    "/register",
    response_model=schemas.UserRead,
    summary="Register a new user",
    description="Creates a new user account. The user must provide valid registration data such as email and password."
)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with the provided registration data.
    """
    try:
        return services.create_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/activate/{token}",
    summary="Activate user account",
    description="Activates a user account using the token sent to the user's email."
)
def activate_account(token: str, db: Session = Depends(get_db)):
    """
    Activate a user's account using the provided token.
    """
    try:
        return services.activate_user_account(db, token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/login",
    response_model=Token,
    summary="Log in a user",
    description="Authenticates the user and returns a JWT access token if the credentials are valid."
)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return an access token.
    """
    try:
        user = authenticate_user(db, user_data)
        access_token = create_access_token(data={"sub": str(user.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get(
    "/me",
    response_model=schemas.UserRead,
    summary="Get current user",
    description="Returns the current authenticated user's information."
)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Get details of the current authenticated user.
    """
    return current_user


@router.post(
    "/change-password",
    summary="Change current user's password",
    description="Allows the authenticated user to change their password by providing the current and new passwords."
)
def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change the password of the current authenticated user.
    """
    try:
        return services.change_password_with_current(db, current_user, current_password, new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/reset-password-request",
    summary="Request password reset",
    description="Initiates a password reset by sending a reset link to the user's email address."
)
def reset_password_request(email: str, new_password: str, db: Session = Depends(get_db)):
    """
    Request a password reset using the user's email.
    """
    try:
        return services.reset_password_request(db, email, new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/reset-password/{token}",
    summary="Reset password with token",
    description="Completes the password reset process using the token sent via email."
)
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    """
    Reset the password using a provided token.
    """
    try:
        return services.reset_password(db, token, new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

