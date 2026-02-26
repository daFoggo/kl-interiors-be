from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from app.routers import (
    health,
    users,
    auth,
    product_categories,
    product_types,
    product_colors,
    product_materials,
    product_collections,
    products,
    bookmarks,
)
from app.database import engine, Base

import contextlib


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="KL Interiors API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(product_categories.router)
app.include_router(product_types.router)
app.include_router(product_colors.router)
app.include_router(product_materials.router)
app.include_router(product_collections.router)
app.include_router(products.router)
app.include_router(bookmarks.router)

add_pagination(app)


@app.get("/")
async def root():
    return {
        "success": True,
        "payload": {"data": {"message": "KL Interiors API is running!"}},
    }
