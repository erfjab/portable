import re
import asyncio
from datetime import datetime, timedelta
from typing import List
from collections import defaultdict
from secrets import token_hex
from src.db import Session, Server, Subscription, MarzneshinTag
from src.clients._manager import ClientManager, MarzneshinUserResponse
from src.clients.marzneshin._models import UserExpireStrategy


class SubscriptionTransfer:
    @classmethod
    def username_creater(cls, username: str) -> str:
        if re.fullmatch(r"^[^_]+_\d{2}$", username):
            username = username.split("_")[0]
        return f"x{username}"

    @classmethod
    async def exports(
        cls, db: Session, *, from_server: Server, to_server: Server
    ) -> list[MarzneshinUserResponse]:
        exports = []
        page = 1
        while True:
            users = None
            for i in range(3):
                try:
                    await asyncio.sleep(1)
                    users = await ClientManager.get_users(
                        server=from_server, page=page, size=100
                    )
                    if users:
                        break
                except Exception:
                    continue
            if not users:
                break

            for user in users:
                username = cls.username_creater(user.username)
                if not Subscription.get_by_username(db, username=username):
                    subscription = Subscription.create(
                        db,
                        key=token_hex(16),
                        username=username,
                        server_id=to_server.id,
                    )
                    MarzneshinTag.create(
                        db,
                        key=user.key,
                        username=user.username,
                        subscription_id=subscription.id,
                    )
                exports.append(user)
            page += 1
            users = None
        return exports

    @classmethod
    async def imports(
        cls, *, server: Server, subscriptions: List[MarzneshinUserResponse]
    ) -> dict[str, int]:
        configs = await ClientManager.get_configs(server=server)
        inbounds = defaultdict(list)
        proxies = {}
        for config in configs:
            inbounds[config.protocol].append(config.tag)
            proxies[config.protocol] = {}

        result = {
            "total": 0,
            "success": 0,
            "failed": 0,
        }

        for sub in subscriptions:
            result["total"] += 1
            username = cls.username_creater(sub.username)
            data = {
                "username": username,
                "data_limit": sub.data_left,
                "proxies": proxies,
                "inbounds": inbounds,
            }
            if sub.expire_strategy == UserExpireStrategy.NEVER:
                data["status"] = "active"
                data["expire"] = 0
            if sub.expire_strategy == UserExpireStrategy.START_ON_FIRST_USE:
                data["status"] = "on_hold"
                data["on_hold_expire_duration"] = sub.usage_duration
            if sub.expire_strategy == UserExpireStrategy.FIXED_DATE:
                data["status"] = "active"
                data["expire"] = (
                    int(sub.expire_date.timestamp())
                    if int(sub.expire_date.timestamp())
                    > int(datetime.now().timestamp())
                    else int((datetime.now() + timedelta(seconds=60)).timestamp())
                )
            for i in range(1):
                try:
                    await asyncio.sleep(1)
                    create_sub = await ClientManager.create_user(
                        data=data, server=server
                    )
                    if create_sub:
                        result["success"] += 1
                        break
                    if i == 1:
                        result["failed"] += 1
                        continue
                except Exception:
                    continue

        return result
