from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

@router.get("/")
async def get_health():
    """
    Health check API
    """
    return {"status": "ok", "message": "API is healthy"}
