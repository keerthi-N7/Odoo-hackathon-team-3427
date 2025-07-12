from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import UserOut, UserUpdate
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from typing import List
import os
from app.schemas import UserOut, UserUpdate


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current user from JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Get all public profiles
@router.get("/", response_model=List[UserOut])
def get_all_profiles(db: Session = Depends(get_db)):
    return db.query(User).filter(User.is_public == True).all()

# Get a single user profile by ID
@router.get("/{user_id}", response_model=UserOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.is_public == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or private")
    return user

# Update current user profile
@router.put("/", response_model=UserOut)
def update_profile(
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.query(User).filter(User.id == current_user.id).update(updates.dict(exclude_unset=True))
    db.commit()
    db.refresh(current_user)
    return current_user
# app/profile.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth import get_current_user

router = APIRouter(prefix="/api/profile", tags=["Profile"])

# Get public profiles
@router.get("/", response_model=list[schemas.UserOut])
def get_public_profiles(db: Session = Depends(database.SessionLocal)):
    return db.query(models.User).filter(models.User.is_public == True).all()

# Get specific profile by ID
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(database.SessionLocal)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or not user.is_public:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update profile (auth required)
@router.put("/", response_model=schemas.UserOut)
def update_profile(
    update_data: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.SessionLocal),
):
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
