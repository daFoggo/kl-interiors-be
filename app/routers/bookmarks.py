from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])

@router.post("/", response_model=schemas.ApiResponse[schemas.BookmarkResponse], status_code=status.HTTP_201_CREATED)
def add_bookmark(bookmark: schemas.BookmarkCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Check if product exists Validate product
    product = db.query(models.Product).filter(models.Product.id == bookmark.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Check if duplicate bookmark
    existing = db.query(models.Bookmark).filter(
        models.Bookmark.product_id == bookmark.product_id,
        models.Bookmark.user_id == current_user.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Product already bookmarked")
        
    new_bookmark = models.Bookmark(user_id=current_user.id, product_id=bookmark.product_id)
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    return schemas.ApiResponse(success=True, payload=new_bookmark)

@router.get("/", response_model=schemas.CustomPage[schemas.BookmarkResponse])
def get_my_bookmarks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return paginate(db, select(models.Bookmark).where(models.Bookmark.user_id == current_user.id))
    
@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_bookmark(bookmark_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    bookmark = db.query(models.Bookmark).filter(
        models.Bookmark.id == bookmark_id,
        models.Bookmark.user_id == current_user.id
    ).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found or you don't have permission")
    
    db.delete(bookmark)
    db.commit()
    return None
