from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class MarzneshinToken(BaseModel):
    access_token: str
    is_sudo: bool
    token_type: str = "bearer"


class MarzneshinAdmin(BaseModel):
    username: str
    is_sudo: bool
    enabled: bool = True

    @property
    def is_active(self) -> bool:
        return self.is_sudo and self.enabled


class UserExpireStrategy(str, Enum):
    NEVER = "never"
    FIXED_DATE = "fixed_date"
    START_ON_FIRST_USE = "start_on_first_use"


class MarzneshinUserResponse(BaseModel):
    username: str
    key: Optional[str]
    is_active: bool
    data_limit: Optional[int]
    used_traffic: int
    owner_username: Optional[str]
    expire_strategy: UserExpireStrategy
    expire_date: Optional[datetime]
    usage_duration: Optional[int]
    activation_deadline: Optional[datetime]
    subscription_url: str

    @property
    def data_left(self) -> int:
        if not self.data_limit:
            return 0
        if not self.used_traffic:
            return self.data_limit
        data_left = int(self.data_limit - self.used_traffic)
        if data_left <= 0:
            return 1024
        return data_left


class MarzneshinServiceResponce(BaseModel):
    id: int
    name: str | None
    inbound_ids: list[int]
    user_ids: list[int]
