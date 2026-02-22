from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class ProductStatusEnum(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

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

class ProductBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    material: Optional[str] = None
    dimensions: Optional[str] = None
    color: Optional[str] = None
    price: float = Field(ge=0.0)
    stock_quantity: int = Field(default=0, ge=0)
    status: ProductStatusEnum = ProductStatusEnum.DRAFT
    is_featured: bool = False
    model_config = ConfigDict(from_attributes=True)

class ProductCreate(ProductBase):
    category_id: UUID

class ProductResponse(ProductBase):
    id: UUID
    category_id: UUID
    created_at: datetime
    updated_at: datetime
    images: List[ProductImageResponse] = []
