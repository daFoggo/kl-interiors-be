import uuid
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base

# join table (M:M): products ↔ product_materials
products_materials = Table(
    "products_materials",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "material_id",
        UUID(as_uuid=True),
        ForeignKey("product_materials.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class ProductMaterial(Base):
    __tablename__ = "product_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)  # e.g. "Gỗ sồi tự nhiên"
    image_url = Column(String, nullable=True)  # texture thumbnail

    products = relationship(
        "Product", secondary="products_materials", back_populates="product_materials"
    )
