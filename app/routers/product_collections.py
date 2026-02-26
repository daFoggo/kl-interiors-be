from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_admin_user
from app.utils import generate_slug

router = APIRouter(prefix="/product-collections", tags=["Product Collections"])


@router.post(
    "/",
    response_model=schemas.ApiResponse[schemas.ProductCollectionResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_product_collection(
    collection: schemas.ProductCollectionCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    slug = collection.slug or generate_slug(collection.name)
    if (
        db.query(models.ProductCollection)
        .filter(models.ProductCollection.slug == slug)
        .first()
    ):
        raise HTTPException(status_code=400, detail="Slug already registered")
    data = collection.model_dump()
    data["slug"] = slug
    new_col = models.ProductCollection(**data)
    db.add(new_col)
    db.commit()
    db.refresh(new_col)
    return schemas.ApiResponse(success=True, payload=new_col)


@router.get(
    "/featured",
    response_model=schemas.ApiResponse[List[schemas.ProductCollectionResponse]],
)
def get_featured_product_collections(
    limit: int = Query(default=6, ge=1, le=20),
    db: Session = Depends(get_db),
):
    cols = (
        db.query(models.ProductCollection)
        .filter(models.ProductCollection.is_featured == True)  # noqa: E712
        .order_by(models.ProductCollection.updated_at.desc())
        .limit(limit)
        .all()
    )
    return schemas.ApiResponse(success=True, payload=cols)


@router.get(
    "/new", response_model=schemas.ApiResponse[List[schemas.ProductCollectionResponse]]
)
def get_new_product_collections(
    limit: int = Query(default=6, ge=1, le=20),
    db: Session = Depends(get_db),
):
    cols = (
        db.query(models.ProductCollection)
        .order_by(models.ProductCollection.created_at.desc())
        .limit(limit)
        .all()
    )
    return schemas.ApiResponse(success=True, payload=cols)


@router.get("/", response_model=schemas.CustomPage[schemas.ProductCollectionResponse])
def get_product_collections(db: Session = Depends(get_db)):
    return paginate(db, select(models.ProductCollection))


@router.get(
    "/{collection_id}",
    response_model=schemas.ApiResponse[schemas.ProductCollectionResponse],
)
def get_product_collection(collection_id: UUID, db: Session = Depends(get_db)):
    col = (
        db.query(models.ProductCollection)
        .filter(models.ProductCollection.id == collection_id)
        .first()
    )
    if not col:
        raise HTTPException(status_code=404, detail="Product collection not found")
    return schemas.ApiResponse(success=True, payload=col)


@router.get(
    "/{collection_id}/products",
    response_model=schemas.CustomPage[schemas.ProductResponse],
)
def get_products_by_collection(collection_id: UUID, db: Session = Depends(get_db)):
    col = (
        db.query(models.ProductCollection)
        .filter(models.ProductCollection.id == collection_id)
        .first()
    )
    if not col:
        raise HTTPException(status_code=404, detail="Product collection not found")
    return paginate(
        db,
        select(models.Product).where(
            models.Product.collections.any(models.ProductCollection.id == collection_id)
        ),
    )


@router.put(
    "/{collection_id}",
    response_model=schemas.ApiResponse[schemas.ProductCollectionResponse],
)
def update_product_collection(
    collection_id: UUID,
    collection_update: schemas.ProductCollectionCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    col = (
        db.query(models.ProductCollection)
        .filter(models.ProductCollection.id == collection_id)
        .first()
    )
    if not col:
        raise HTTPException(status_code=404, detail="Product collection not found")
    update_data = collection_update.model_dump(exclude_unset=True)
    new_slug = update_data.get("slug") or (
        generate_slug(update_data["name"]) if "name" in update_data else None
    )
    if new_slug and new_slug != col.slug:
        if (
            db.query(models.ProductCollection)
            .filter(models.ProductCollection.slug == new_slug)
            .first()
        ):
            raise HTTPException(status_code=400, detail="Slug already registered")
        update_data["slug"] = new_slug
    for key, value in update_data.items():
        setattr(col, key, value)
    db.commit()
    db.refresh(col)
    return schemas.ApiResponse(success=True, payload=col)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_collection(
    collection_id: UUID,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    col = (
        db.query(models.ProductCollection)
        .filter(models.ProductCollection.id == collection_id)
        .first()
    )
    if not col:
        raise HTTPException(status_code=404, detail="Product collection not found")
    db.delete(col)
    db.commit()
    return None
