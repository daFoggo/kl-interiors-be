from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class ProductTypeBase(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: bool = False

    model_config = ConfigDict(from_attributes=True)


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeResponse(ProductTypeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
