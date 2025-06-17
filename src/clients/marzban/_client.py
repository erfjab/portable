from typing import Optional
from ..core import ClientBase, RequestCore
from ._models import (
    MarzbanAdmin,
    MarzbanProxyInbound,
    MarzbanToken,
    MarzbanUserResponse,
)


class MarzbanClient(ClientBase, RequestCore):
    def __init__(self, host: str):
        super().__init__(host)

    async def generate_access_token(
        self, *, username: str, password: str
    ) -> Optional[MarzbanToken]:
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        return await self.post(
            endpoint="/api/admin/token",
            data=data,
            response_model=MarzbanToken,
        )

    async def get_admin(self, *, username: str, access: str) -> Optional[MarzbanAdmin]:
        return await self.get(
            endpoint=f"/api/admin/{username}",
            access_token=access,
            response_model=MarzbanAdmin,
        )

    async def get_configs(self, *, access: str) -> Optional[list[MarzbanProxyInbound]]:
        inbounds: dict = await self.get(endpoint="/api/inbounds", access_token=access)
        if not inbounds:
            return None
        return [
            MarzbanProxyInbound(**inbound)
            for inbound_list in inbounds.values()
            for inbound in (
                inbound_list if isinstance(inbound_list, list) else [inbound_list]
            )
        ]

    async def get_user(
        self, *, username: str, access: str
    ) -> Optional[MarzbanUserResponse]:
        return await self.get(
            endpoint=f"/api/user/{username}",
            access_token=access,
            response_model=MarzbanUserResponse,
        )

    async def get_users(
        self, *, access: str, size: int, page: int
    ) -> Optional[list[MarzbanUserResponse]]:
        users = await self.get(
            endpoint="/api/users",
            params={
                "offset": ((page - 1) * size),
                "limit": size,
            },
            access_token=access,
        )
        if not users:
            return False
        return [MarzbanUserResponse(**user) for user in users["users"]]

    async def create_user(
        self, data: dict, access: str
    ) -> Optional[MarzbanUserResponse]:
        return await self.post(
            endpoint="/api/user",
            access_token=access,
            data=data,
            response_model=MarzbanUserResponse,
        )

    async def update_user(
        self, *, username: str, data: dict, access: str
    ) -> Optional[MarzbanUserResponse]:
        return await self.put(
            endpoint=f"/api/user/{username}",
            access_token=access,
            data=data,
            response_model=MarzbanUserResponse,
        )

    async def remove_user(self, *, username: str, access: str) -> bool:
        return await self.delete(
            endpoint=f"/api/user/{username}",
            access_token=access,
        )
