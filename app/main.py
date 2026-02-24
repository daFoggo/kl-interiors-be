from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, users, auth, categories, products, bookmarks
from app.database import engine, Base

import contextlib

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="KL Interiors API", lifespan=lifespan)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include Routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(bookmarks.router)

@app.get("/")
async def root():
    return {"message": "KL Interiors API is running!"}
