from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_admin_user
from app.utils import generate_slug

router = APIRouter(prefix="/products", tags=["Products"])


def _resolve_colors(db: Session, color_ids: list[UUID]) -> list[models.ProductColor]:
    colors = (
        db.query(models.ProductColor)
        .filter(models.ProductColor.id.in_(color_ids))
        .all()
    )
    if len(colors) != len(color_ids):
        raise HTTPException(status_code=400, detail="One or more color IDs are invalid")
    return colors


def _resolve_materials(
    db: Session, material_ids: list[UUID]
) -> list[models.ProductMaterial]:
    materials = (
        db.query(models.ProductMaterial)
        .filter(models.ProductMaterial.id.in_(material_ids))
        .all()
    )
    if len(materials) != len(material_ids):
        raise HTTPException(
            status_code=400, detail="One or more material IDs are invalid"
        )
    return materials


def _resolve_collections(
    db: Session, collection_ids: list[UUID]
) -> list[models.ProductCollection]:
    collections = (
        db.query(models.ProductCollection)
        .filter(models.ProductCollection.id.in_(collection_ids))
        .all()
    )
    if len(collections) != len(collection_ids):
        raise HTTPException(
            status_code=400, detail="One or more collection IDs are invalid"
        )
    return collections


@router.post(
    "/",
    response_model=schemas.ApiResponse[schemas.ProductResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    slug = product.slug or generate_slug(product.name)
    if db.query(models.Product).filter(models.Product.slug == slug).first():
        raise HTTPException(status_code=400, detail="Slug already registered")

    if (
        not db.query(models.ProductCategory)
        .filter(models.ProductCategory.id == product.product_category_id)
        .first()
    ):
        raise HTTPException(status_code=400, detail="Invalid category ID")

    product_colors = _resolve_colors(db, product.product_color_ids)
    product_materials = _resolve_materials(db, product.product_material_ids)
    product_collections = _resolve_collections(db, product.product_collection_ids)

    product_data = product.model_dump(
        exclude={"product_color_ids", "product_material_ids", "product_collection_ids"}
    )
    product_data["slug"] = slug
    new_product = models.Product(**product_data)
    new_product.product_colors = product_colors
    new_product.product_materials = product_materials
    new_product.product_collections = product_collections

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return schemas.ApiResponse(success=True, payload=new_product)


@router.get("/", response_model=schemas.CustomPage[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return paginate(db, select(models.Product))


@router.get(
    "/{product_id}", response_model=schemas.ApiResponse[schemas.ProductResponse]
)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.ApiResponse(success=True, payload=product)


@router.put(
    "/{product_id}", response_model=schemas.ApiResponse[schemas.ProductResponse]
)
def update_product(
    product_id: UUID,
    product_update: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.model_dump(
        exclude_unset=True,
        exclude={"product_color_ids", "product_material_ids", "product_collection_ids"},
    )
    for key, value in update_data.items():
        setattr(product, key, value)

    if product_update.product_color_ids is not None:
        product.product_colors = _resolve_colors(db, product_update.product_color_ids)
    if product_update.product_material_ids is not None:
        product.product_materials = _resolve_materials(
            db, product_update.product_material_ids
        )
    if product_update.product_collection_ids is not None:
        product.product_collections = _resolve_collections(
            db, product_update.product_collection_ids
        )

    db.commit()
    db.refresh(product)
    return schemas.ApiResponse(success=True, payload=product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return None
