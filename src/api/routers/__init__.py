from fastapi import APIRouter
from . import _telegram, _subscription


def setup_routers() -> APIRouter:
    router = APIRouter()
    router.include_router(_telegram.router)
    router.include_router(_subscription.router)
    return router


__all__ = ["setup_routers"]
