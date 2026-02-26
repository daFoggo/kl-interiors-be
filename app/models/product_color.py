import uuid
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base

# join table (M:M): products ↔ product_colors
products_colors = Table(
    "products_colors",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "color_id",
        UUID(as_uuid=True),
        ForeignKey("product_colors.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class ProductColor(Base):
    __tablename__ = "product_colors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)  # e.g. "Nâu sậm"
    hex_code = Column(String(7), nullable=True)  # e.g. "#5C3317"

    products = relationship(
        "Product", secondary="products_colors", back_populates="colors"
    )
