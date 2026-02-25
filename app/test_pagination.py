import asyncio
from typing import Generic, TypeVar, Any, Sequence

from fastapi import FastAPI
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.default import Params
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationMeta(BaseModel):
    page: int
    size: int
    total: int
    pages: int

class PaginatedPayload(BaseModel, Generic[T]):
    pagination: PaginationMeta
    data: list[T]

class CustomPage(AbstractPage[T], Generic[T]):
    success: bool = True
    payload: PaginatedPayload[T]

    __params_type__ = Params

    @classmethod
    def create(cls, items: Sequence[T], params: Params, total: int, **kwargs: Any) -> "CustomPage[T]":
        pages = (total + params.size - 1) // params.size if total > 0 else 0
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

app = FastAPI()
add_pagination(app)

@app.get("/test", response_model=CustomPage[int])
def test_endpoint():
    return paginate([1, 2, 3])

if __name__ == "__main__":
    import json
    # Run test_endpoint to see output
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/test")
    print("STATUS", response.status_code)
    print("JSON", json.dumps(response.json(), indent=2))
