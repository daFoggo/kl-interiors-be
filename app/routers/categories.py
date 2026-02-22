from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_admin_user

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    db_category = db.query(models.Category).filter(models.Category.slug == category.slug).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Slug already registered")
    
    new_category = models.Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=List[schemas.CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/{category_id}/products", response_model=List[schemas.ProductResponse])
def get_category_products(category_id: UUID, db: Session = Depends(get_db)):
    """Proper RESTful endpoint representing Resource Hierarchy"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    return category.products

@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(category_id: UUID, category_update: schemas.CategoryCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    update_data = category_update.model_dump(exclude_unset=True)
    if "slug" in update_data and update_data["slug"] != category.slug:
        db_category = db.query(models.Category).filter(models.Category.slug == update_data["slug"]).first()
        if db_category:
            raise HTTPException(status_code=400, detail="Slug already registered")
            
    for key, value in update_data.items():
        setattr(category, key, value)
        
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: UUID, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    db.delete(category)
    db.commit()
    return None
