from fastapi import APIRouter

from routers import api

router = APIRouter()

router.include_router(api.router)
