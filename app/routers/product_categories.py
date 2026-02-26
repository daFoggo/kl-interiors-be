from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_admin_user
from app.utils import generate_slug

router = APIRouter(prefix="/product-categories", tags=["Product Categories"])


@router.post(
    "/",
    response_model=schemas.ApiResponse[schemas.ProductCategoryResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_product_category(
    category: schemas.ProductCategoryCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    slug = category.slug or generate_slug(category.name)
    if (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.slug == slug)
        .first()
    ):
        raise HTTPException(status_code=400, detail="Slug already registered")

    data = category.model_dump()
    data["slug"] = slug
    new_cat = models.ProductCategory(**data)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return schemas.ApiResponse(success=True, payload=new_cat)


@router.get(
    "/popular",
    response_model=schemas.ApiResponse[List[schemas.ProductCategoryResponse]],
)
def get_popular_product_categories(
    limit: int = Query(default=6, ge=1, le=20),
    db: Session = Depends(get_db),
):
    product_count_subq = (
        select(
            models.Product.product_category_id,
            func.count(models.Product.id).label("product_count"),
        )
        .group_by(models.Product.product_category_id)
        .subquery()
    )
    bookmark_count_subq = (
        select(
            models.Product.product_category_id,
            func.count(models.Bookmark.id).label("bookmark_count"),
        )
        .join(
            models.Bookmark,
            models.Bookmark.product_id == models.Product.id,
            isouter=True,
        )
        .group_by(models.Product.product_category_id)
        .subquery()
    )
    results = (
        db.query(models.ProductCategory)
        .outerjoin(
            product_count_subq,
            product_count_subq.c.product_category_id == models.ProductCategory.id,
        )
        .outerjoin(
            bookmark_count_subq,
            bookmark_count_subq.c.product_category_id == models.ProductCategory.id,
        )
        .order_by(
            (
                func.coalesce(product_count_subq.c.product_count, 0)
                + func.coalesce(bookmark_count_subq.c.bookmark_count, 0)
            ).desc()
        )
        .limit(limit)
        .all()
    )
    return schemas.ApiResponse(success=True, payload=results)


@router.get("/", response_model=schemas.CustomPage[schemas.ProductCategoryResponse])
def get_product_categories(db: Session = Depends(get_db)):
    return paginate(db, select(models.ProductCategory))


@router.get(
    "/{category_id}",
    response_model=schemas.ApiResponse[schemas.ProductCategoryResponse],
)
def get_product_category(category_id: UUID, db: Session = Depends(get_db)):
    cat = (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.id == category_id)
        .first()
    )
    if not cat:
        raise HTTPException(status_code=404, detail="Product category not found")
    return schemas.ApiResponse(success=True, payload=cat)


@router.get(
    "/{category_id}/products",
    response_model=schemas.CustomPage[schemas.ProductResponse],
)
def get_products_by_category(category_id: UUID, db: Session = Depends(get_db)):
    cat = (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.id == category_id)
        .first()
    )
    if not cat:
        raise HTTPException(status_code=404, detail="Product category not found")
    return paginate(
        db, select(models.Product).where(models.Product.product_category_id == category_id)
    )


@router.put(
    "/{category_id}",
    response_model=schemas.ApiResponse[schemas.ProductCategoryResponse],
)
def update_product_category(
    category_id: UUID,
    category_update: schemas.ProductCategoryCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    cat = (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.id == category_id)
        .first()
    )
    if not cat:
        raise HTTPException(status_code=404, detail="Product category not found")

    update_data = category_update.model_dump(exclude_unset=True)
    new_slug = update_data.get("slug") or (
        generate_slug(update_data["name"]) if "name" in update_data else None
    )
    if new_slug and new_slug != cat.slug:
        if (
            db.query(models.ProductCategory)
            .filter(models.ProductCategory.slug == new_slug)
            .first()
        ):
            raise HTTPException(status_code=400, detail="Slug already registered")
        update_data["slug"] = new_slug
    elif new_slug:
        update_data.pop("slug", None)

    for key, value in update_data.items():
        setattr(cat, key, value)
    db.commit()
    db.refresh(cat)
    return schemas.ApiResponse(success=True, payload=cat)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    cat = (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.id == category_id)
        .first()
    )
    if not cat:
        raise HTTPException(status_code=404, detail="Product category not found")
    db.delete(cat)
    db.commit()
    return None
