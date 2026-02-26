from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class ProductCategoryBase(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: bool = False
    parent_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryResponse(ProductCategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
