from eiogram import Router
from . import _commands  # noqa
from ._middlewares import AdminMiddleware
from .servers import setup_servers_router


def setup_admin_routers() -> Router:
    router = Router()
    router.include_router(_commands.router)
    router.include_router(setup_servers_router())
    router.middleware.register(AdminMiddleware())
    return router


__all__ = ["setup_admin_routers"]
