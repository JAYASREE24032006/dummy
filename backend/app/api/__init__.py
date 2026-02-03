from fastapi import APIRouter

router = APIRouter()

# Import auth routes later
from app.auth import oidc
router.include_router(oidc.router, prefix="/auth", tags=["auth"])

