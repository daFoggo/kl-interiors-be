from fastapi import APIRouter
from app import schemas

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

@router.get("/", response_model=schemas.ApiResponse[dict])
async def get_health():
    """
    Health check API
    """
    return schemas.ApiResponse(success=True, payload={"status": "ok", "message": "API is healthy"})
