from fastapi import APIRouter

from routers.api.v1 import monitoring, user

router = APIRouter()

router.include_router(monitoring.router, tags=["monitoring"])
router.include_router(user.router, tags=["user"])
