from typing import Optional, Union
from src.db import ServerType, Server
from .marzneshin import (
    MarzneshinClient,
    MarzneshinAdmin,
    MarzneshinUserResponse,
    MarzneshinServiceResponce,
)
from .marzban import (
    MarzbanClient,
    MarzbanAdmin,
    MarzbanUserResponse,
    MarzbanProxyInbound,
)


class ClientManager:
    @classmethod
    async def generate_access_token(
        self, *, config: dict[str, str], server_type: ServerType
    ) -> Optional[str]:
        match server_type:
            case ServerType.MARZNESHIN:
                api = MarzneshinClient(config["host"])
                token = await api.generate_access_token(
                    username=config["username"], password=config["password"]
                )
                token = token.access_token if token else None
            case ServerType.MARZBAN:
                api = MarzbanClient(config["host"])
                token = await api.generate_access_token(
                    username=config["username"], password=config["password"]
                )
                token = token.access_token if token else None
            case _:
                return

        return token

    @classmethod
    async def get_admin(
        self, *, username: str, server: Server
    ) -> Optional[Union[MarzbanAdmin, MarzneshinAdmin]]:
        match server.type:
            case ServerType.MARZNESHIN:
                api = MarzneshinClient(server.config["host"])
                admin = await api.get_admin(username=username, access=server.access)
            case ServerType.MARZBAN:
                api = MarzbanClient(server.config["host"])
                admin = await api.get_admin(username=username, access=server.access)
            case _:
                return

        return admin

    @classmethod
    async def get_configs(
        self, *, server: Server
    ) -> Optional[list[Union[MarzneshinServiceResponce, MarzbanProxyInbound]]]:
        match server.type:
            case ServerType.MARZNESHIN:
                api = MarzneshinClient(server.config["host"])
                configs = await api.get_configs(access=server.access)
            case ServerType.MARZBAN:
                api = MarzbanClient(server.config["host"])
                configs = await api.get_configs(access=server.access)
            case _:
                return

        return configs

    @classmethod
    async def get_user(
        self, *, username: str, server: Server
    ) -> Optional[Union[MarzneshinUserResponse, MarzbanUserResponse]]:
        match server.type:
            case ServerType.MARZNESHIN:
                api = MarzneshinClient(server.config["host"])
                user = await api.get_user(username=username, access=server.access)
            case ServerType.MARZBAN:
                api = MarzbanClient(server.config["host"])
                user = await api.get_user(username=username, access=server.access)
            case _:
                return

        return user

    @classmethod
    async def get_users(
        self, *, server: Server, page: int = 1, size: int = 50
    ) -> Optional[list[Union[MarzbanUserResponse, MarzneshinUserResponse]]]:
        match server.type:
            case ServerType.MARZNESHIN:
                api = MarzneshinClient(server.config["host"])
                users = await api.get_users(access=server.access, page=page, size=size)
            case ServerType.MARZBAN:
                api = MarzbanClient(server.config["host"])
                users = await api.get_users(access=server.access, page=page, size=size)
            case _:
                return

        return users

    @classmethod
    async def create_user(
        self, *, data: dict, server: Server
    ) -> Optional[Union[MarzneshinUserResponse, MarzbanUserResponse]]:
        match server.type:
            case ServerType.MARZNESHIN:
                api = MarzneshinClient(server.config["host"])
                user = await api.create_user(
                    username=data["username"], data=data, access=server.access
                )
            case ServerType.MARZBAN:
                api = MarzbanClient(server.config["host"])
                user = await api.create_user(
                    username=data["username"], data=data, access=server.access
                )
            case _:
                return

        return user

    @classmethod
    async def update_user(
        self, *, data: dict, server: Server
    ) -> Optional[Union[MarzneshinUserResponse, MarzbanUserResponse]]:
        match server.type:
            case ServerType.MARZNESHIN:
                api = MarzneshinClient(server.config["host"])
                user = await api.update_user(
                    username=data["username"], data=data, access=server.access
                )
            case ServerType.MARZBAN:
                api = MarzbanClient(server.config["host"])
                user = await api.update_user(
                    username=data["username"], data=data, access=server.access
                )
            case _:
                return

        return user

    @classmethod
    async def remove_user(self, *, username: str, server: Server) -> Optional[bool]:
        match server.type:
            case ServerType.MARZNESHIN:
                api = MarzneshinClient(server.config["host"])
                action = await api.remove_user(username=username, access=server.access)
            case ServerType.MARZBAN:
                api = MarzbanClient(server.config["host"])
                action = await api.remove_user(username=username, access=server.access)
            case _:
                return

        return action
