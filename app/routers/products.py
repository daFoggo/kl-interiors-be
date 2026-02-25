from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_admin_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=schemas.ApiResponse[schemas.ProductResponse], status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    db_product = db.query(models.Product).filter(models.Product.slug == product.slug).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Slug already registered")
        
    category = db.query(models.Category).filter(models.Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid Category ID")
        
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return schemas.ApiResponse(success=True, payload=new_product)

@router.get("/", response_model=schemas.CustomPage[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return paginate(db, select(models.Product))

@router.get("/{product_id}", response_model=schemas.ApiResponse[schemas.ProductResponse])
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.ApiResponse(success=True, payload=product)

@router.put("/{product_id}", response_model=schemas.ApiResponse[schemas.ProductResponse])
def update_product(product_id: UUID, product_update: schemas.ProductCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
        
    db.commit()
    db.refresh(product)
    return schemas.ApiResponse(success=True, payload=product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: UUID, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    db.delete(product)
    db.commit()
    return None
