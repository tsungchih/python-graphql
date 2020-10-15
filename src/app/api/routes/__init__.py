from fastapi import APIRouter
from app.core.config import API_PREFIX
from app.api.routes import (
    health,
    hello,
    pm25,
    root,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["healthcheck"], prefix=API_PREFIX)
api_router.include_router(hello.router, tags=["helloworld"], prefix=API_PREFIX)
api_router.include_router(pm25.router, tags=["environment"], prefix=API_PREFIX)
api_router.include_router(root.router, tags=["root"], prefix=API_PREFIX)