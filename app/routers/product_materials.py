from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_admin_user

router = APIRouter(prefix="/product-materials", tags=["Product Materials"])


@router.post(
    "/",
    response_model=schemas.ApiResponse[schemas.ProductMaterialResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_product_material(
    material: schemas.ProductMaterialCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    if (
        db.query(models.ProductMaterial)
        .filter(models.ProductMaterial.name == material.name)
        .first()
    ):
        raise HTTPException(status_code=400, detail="Material name already exists")
    new_material = models.ProductMaterial(**material.model_dump())
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return schemas.ApiResponse(success=True, payload=new_material)


@router.get(
    "/", response_model=schemas.ApiResponse[List[schemas.ProductMaterialResponse]]
)
def get_product_materials(db: Session = Depends(get_db)):
    materials = (
        db.query(models.ProductMaterial).order_by(models.ProductMaterial.name).all()
    )
    return schemas.ApiResponse(success=True, payload=materials)


@router.get(
    "/{material_id}",
    response_model=schemas.ApiResponse[schemas.ProductMaterialResponse],
)
def get_product_material(material_id: UUID, db: Session = Depends(get_db)):
    material = (
        db.query(models.ProductMaterial)
        .filter(models.ProductMaterial.id == material_id)
        .first()
    )
    if not material:
        raise HTTPException(status_code=404, detail="Product material not found")
    return schemas.ApiResponse(success=True, payload=material)


@router.put(
    "/{material_id}",
    response_model=schemas.ApiResponse[schemas.ProductMaterialResponse],
)
def update_product_material(
    material_id: UUID,
    material_update: schemas.ProductMaterialCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    material = (
        db.query(models.ProductMaterial)
        .filter(models.ProductMaterial.id == material_id)
        .first()
    )
    if not material:
        raise HTTPException(status_code=404, detail="Product material not found")
    for key, value in material_update.model_dump(exclude_unset=True).items():
        setattr(material, key, value)
    db.commit()
    db.refresh(material)
    return schemas.ApiResponse(success=True, payload=material)


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_material(
    material_id: UUID,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    material = (
        db.query(models.ProductMaterial)
        .filter(models.ProductMaterial.id == material_id)
        .first()
    )
    if not material:
        raise HTTPException(status_code=404, detail="Product material not found")
    db.delete(material)
    db.commit()
    return None
