from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_admin_user
from app.utils import generate_slug

router = APIRouter(prefix="/product-types", tags=["Product Types"])


@router.post("/", response_model=schemas.ApiResponse[schemas.ProductTypeResponse], status_code=status.HTTP_201_CREATED)
def create_product_type(
    product_type: schemas.ProductTypeCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    slug = product_type.slug or generate_slug(product_type.name)
    if db.query(models.ProductType).filter(models.ProductType.slug == slug).first():
        raise HTTPException(status_code=400, detail="Slug already registered")

    data = product_type.model_dump()
    data["slug"] = slug
    new_type = models.ProductType(**data)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return schemas.ApiResponse(success=True, payload=new_type)


@router.get("/", response_model=schemas.ApiResponse[List[schemas.ProductTypeResponse]])
def get_product_types(db: Session = Depends(get_db)):
    types = db.query(models.ProductType).order_by(models.ProductType.name).all()
    return schemas.ApiResponse(success=True, payload=types)


@router.get("/{type_id}", response_model=schemas.ApiResponse[schemas.ProductTypeResponse])
def get_product_type(type_id: UUID, db: Session = Depends(get_db)):
    product_type = db.query(models.ProductType).filter(models.ProductType.id == type_id).first()
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    return schemas.ApiResponse(success=True, payload=product_type)


@router.put("/{type_id}", response_model=schemas.ApiResponse[schemas.ProductTypeResponse])
def update_product_type(
    type_id: UUID,
    product_type_update: schemas.ProductTypeCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    product_type = db.query(models.ProductType).filter(models.ProductType.id == type_id).first()
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")

    update_data = product_type_update.model_dump(exclude_unset=True)

    new_slug = update_data.get("slug") or (generate_slug(update_data["name"]) if "name" in update_data else None)
    if new_slug and new_slug != product_type.slug:
        if db.query(models.ProductType).filter(models.ProductType.slug == new_slug).first():
            raise HTTPException(status_code=400, detail="Slug already registered")
        update_data["slug"] = new_slug
    elif new_slug:
        update_data.pop("slug", None)

    for key, value in update_data.items():
        setattr(product_type, key, value)

    db.commit()
    db.refresh(product_type)
    return schemas.ApiResponse(success=True, payload=product_type)


@router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_type(
    type_id: UUID,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    product_type = db.query(models.ProductType).filter(models.ProductType.id == type_id).first()
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")

    db.delete(product_type)
    db.commit()
    return None
