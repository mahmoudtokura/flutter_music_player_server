from fastapi import Depends, HTTPException, status, APIRouter
import uuid
import bcrypt

from database import get_db
from middleware.auth_middleware import auth_middleware
from models.user import User
from pydantic_schemas.user_create import UserCreate
from sqlalchemy.orm import Session, joinedload

from pydantic_schemas.user_login import UserLogin
import jwt

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup_user(user: UserCreate, db: Session = Depends(get_db)) -> dict:
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    # converting password to array of bytes
    bytes = user.password.encode("utf-8")

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    db_user = User(
        id=f"user_id_{str(uuid.uuid4())}",
        name=user.name,
        email=user.email,
        hashed_password=hash,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
    }


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user: UserLogin, db: Session = Depends(get_db)) -> dict:
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check your email or password",
        )
    if not bcrypt.checkpw(user.password.encode("utf-8"), db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check your email or password",
        )

    token = jwt.encode({"id": db_user.id}, "test_password_key")

    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "token": token,
    }


@router.post("/", status_code=status.HTTP_200_OK)
def current_user_data(
    db: Session = Depends(get_db),
    user_dict=Depends(auth_middleware),
):
    db_user = (
        db.query(User)
        .filter(User.id == user_dict["uid"])
        .options(joinedload(User.favorites))
        .first()
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "favorites": db_user.favorites,
    }
