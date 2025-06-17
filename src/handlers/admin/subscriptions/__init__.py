from eiogram import Router
from . import _menu, _info, _operation


def setup_subscriptions_router() -> Router:
    router = Router()
    router.include_router(_menu.router)
    router.include_router(_info.router)
    router.include_router(_operation.router)
    return router


__all__ = ["setup_subscriptions_router"]
