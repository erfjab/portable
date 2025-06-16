from typing import Optional
from ..core import ClientBase, RequestCore
from ._models import MarzneshinAdmin, MarzneshinToken, MarzneshinUserResponse


class MarzneshinClient(ClientBase, RequestCore):
    def __init__(self, host: str):
        super().__init__(host)

    async def generate_access_token(
        self, *, username: str, password: str
    ) -> Optional[MarzneshinToken]:
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        return await self.post(
            endpoint="/api/admins/token",
            data=data,
            response_model=MarzneshinToken,
        )

    async def get_admin(
        self, *, username: str, access: str
    ) -> Optional[MarzneshinAdmin]:
        return await self.get(
            endpoint=f"/api/admins/{username}",
            access=access,
            response_model=MarzneshinAdmin,
        )

    def get_configs(self):
        pass

    async def get_user(
        self, *, username: str, access: str
    ) -> Optional[MarzneshinUserResponse]:
        return await self.get(
            endpoint=f"/api/users/{username}",
            access_token=access,
            response_model=MarzneshinUserResponse,
        )

    async def get_users(
        self, *, access: str, size: int, page: int
    ) -> Optional[list[MarzneshinUserResponse]]:
        users = await self.get(
            endpoint="/api/users",
            params={
                "page": page,
                "size": size,
            },
            access_token=access,
        )
        if not users:
            return
        return [MarzneshinUserResponse(**user) for user in users]

    def create_user(self):
        pass

    def update_user(self):
        pass

    def remove_user(self):
        pass
