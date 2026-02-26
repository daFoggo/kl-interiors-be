from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from uuid import UUID
from enum import Enum

if TYPE_CHECKING:
    from app.schemas.product_type import ProductTypeResponse
    from app.schemas.product_category import ProductCategoryResponse
    from app.schemas.product_color import ProductColorResponse
    from app.schemas.product_material import ProductMaterialResponse
    from app.schemas.product_collection import ProductCollectionResponse


class ProductStatusEnum(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


# ── Product Image ──────────────────────────────────────────────────────────────
class ProductImageBase(BaseModel):
    image_url: str
    is_primary: bool = False
    display_order: int = 0
    model_config = ConfigDict(from_attributes=True)


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageResponse(ProductImageBase):
    id: UUID
    product_id: UUID
    created_at: datetime


# ── Product ────────────────────────────────────────────────────────────────────
class ProductBase(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    dimensions: Optional[str] = None
    price: float = Field(ge=0.0)
    stock_quantity: int = Field(default=0, ge=0)
    status: ProductStatusEnum = ProductStatusEnum.DRAFT
    is_featured: bool = False
    product_type_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    product_category_id: UUID
    product_color_ids: List[UUID] = []
    product_material_ids: List[UUID] = []
    product_collection_ids: List[UUID] = []


class ProductResponse(ProductBase):
    id: UUID
    product_category_id: UUID
    created_at: datetime
    updated_at: datetime
    images: List[ProductImageResponse] = []
    product_colors: List["ProductColorResponse"] = []
    product_materials: List["ProductMaterialResponse"] = []
    product_collections: List["ProductCollectionResponse"] = []
    product_type: Optional["ProductTypeResponse"] = None
    product_category: Optional["ProductCategoryResponse"] = None


# Resolve forward refs
from app.schemas.product_type import ProductTypeResponse  # noqa: E402
from app.schemas.product_category import ProductCategoryResponse  # noqa: E402
from app.schemas.product_color import ProductColorResponse  # noqa: E402
from app.schemas.product_material import ProductMaterialResponse  # noqa: E402
from app.schemas.product_collection import ProductCollectionResponse  # noqa: E402

ProductResponse.model_rebuild()
