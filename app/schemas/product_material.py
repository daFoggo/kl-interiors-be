from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID


class ProductMaterialBase(BaseModel):
    name: str
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ProductMaterialCreate(ProductMaterialBase):
    pass


class ProductMaterialResponse(ProductMaterialBase):
    id: UUID
