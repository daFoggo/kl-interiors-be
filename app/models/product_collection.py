import uuid
from sqlalchemy import Column, String, DateTime, Text, Table, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.utils import utc_now
from app.database import Base

# join table (M:M): products ↔ product_collections
products_collections = Table(
    "products_collections",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "collection_id",
        UUID(as_uuid=True),
        ForeignKey("product_collections.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class ProductCollection(Base):
    __tablename__ = "product_collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)  # banner/cover image
    is_featured = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    products = relationship(
        "Product", secondary="products_collections", back_populates="collections"
    )
