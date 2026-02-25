from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate

from app import models, schemas, auth
import urllib.parse
from app.database import get_db
from app.dependencies import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=schemas.ApiResponse[schemas.UserResponse], status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.email:
        db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user_email:
            raise HTTPException(status_code=400, detail="Email already registered")
            
    if user.phone_number:
        db_user_phone = db.query(models.User).filter(models.User.phone_number == user.phone_number).first()
        if db_user_phone:
            raise HTTPException(status_code=400, detail="Phone number already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    
    avatar_url = user.avatar_url
    if not avatar_url:
        encoded_name = urllib.parse.quote(user.full_name)
        avatar_url = f"https://api.dicebear.com/9.x/lorelei/svg?seed={encoded_name}"
    
    new_user = models.User(
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name,
        phone_number=user.phone_number,
        avatar_url=avatar_url,
        role=schemas.RoleEnum.CUSTOMER.value
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return schemas.ApiResponse(success=True, payload=new_user)

@router.get("/me", response_model=schemas.ApiResponse[schemas.UserResponse])
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return schemas.ApiResponse(success=True, payload=current_user)

@router.get("/", response_model=schemas.CustomPage[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    """Only admins can view all users"""
    return paginate(db, select(models.User))

@router.get("/{user_id}", response_model=schemas.ApiResponse[schemas.UserResponse])
def get_user(user_id: UUID, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    """Only admins can query specific user details by ID"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.ApiResponse(success=True, payload=user)
