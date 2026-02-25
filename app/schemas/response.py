from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, Any, Sequence
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.default import Params

T = TypeVar("T")

class PaginationMeta(BaseModel):
    """Pagination metadata included in paginated responses."""
    page: int
    size: int
    total: int
    pages: int

class PaginatedPayload(BaseModel, Generic[T]):
    """Payload wrapper for paginated list responses."""
    pagination: PaginationMeta
    data: list[T]

class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper for ALL single endpoints."""
    success: bool = True
    payload: T

class CustomPage(AbstractPage[T], Generic[T]):
    """Standard API paginated response"""
    __params_type__ = Params
    
    success: bool = True
    payload: PaginatedPayload[T]

    @classmethod
    def create(cls, items: Sequence[T], params: Params, total: int, **kwargs: Any) -> "CustomPage[T]":
        pages = (total + params.size - 1) // params.size if total > 0 and params.size > 0 else 0
        return cls(
            success=True,
            payload=PaginatedPayload(
                pagination=PaginationMeta(
                    page=params.page,
                    size=params.size,
                    total=total,
                    pages=pages,
                ),
                data=items
            )
        )
