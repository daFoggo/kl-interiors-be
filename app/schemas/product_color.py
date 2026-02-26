from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID


class ProductColorBase(BaseModel):
    name: str
    hex_code: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ProductColorCreate(ProductColorBase):
    pass


class ProductColorResponse(ProductColorBase):
    id: UUID
