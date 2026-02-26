from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from uuid import UUID

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_admin_user
from app.utils import generate_slug

router = APIRouter(prefix="/product-colors", tags=["Product Colors"])


@router.post(
    "/",
    response_model=schemas.ApiResponse[schemas.ProductColorResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_product_color(
    color: schemas.ProductColorCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    if (
        db.query(models.ProductColor)
        .filter(models.ProductColor.name == color.name)
        .first()
    ):
        raise HTTPException(status_code=400, detail="Color name already exists")
    new_color = models.ProductColor(**color.model_dump())
    db.add(new_color)
    db.commit()
    db.refresh(new_color)
    return schemas.ApiResponse(success=True, payload=new_color)


@router.get("/", response_model=schemas.ApiResponse[List[schemas.ProductColorResponse]])
def get_product_colors(db: Session = Depends(get_db)):
    colors = db.query(models.ProductColor).order_by(models.ProductColor.name).all()
    return schemas.ApiResponse(success=True, payload=colors)


@router.get(
    "/{color_id}", response_model=schemas.ApiResponse[schemas.ProductColorResponse]
)
def get_product_color(color_id: UUID, db: Session = Depends(get_db)):
    color = (
        db.query(models.ProductColor).filter(models.ProductColor.id == color_id).first()
    )
    if not color:
        raise HTTPException(status_code=404, detail="Product color not found")
    return schemas.ApiResponse(success=True, payload=color)


@router.put(
    "/{color_id}", response_model=schemas.ApiResponse[schemas.ProductColorResponse]
)
def update_product_color(
    color_id: UUID,
    color_update: schemas.ProductColorCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    color = (
        db.query(models.ProductColor).filter(models.ProductColor.id == color_id).first()
    )
    if not color:
        raise HTTPException(status_code=404, detail="Product color not found")
    for key, value in color_update.model_dump(exclude_unset=True).items():
        setattr(color, key, value)
    db.commit()
    db.refresh(color)
    return schemas.ApiResponse(success=True, payload=color)


@router.delete("/{color_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_color(
    color_id: UUID,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    color = (
        db.query(models.ProductColor).filter(models.ProductColor.id == color_id).first()
    )
    if not color:
        raise HTTPException(status_code=404, detail="Product color not found")
    db.delete(color)
    db.commit()
    return None
