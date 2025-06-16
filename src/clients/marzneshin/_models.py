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


class UserDataUsageResetStrategy(str, Enum):
    no_reset = "no_reset"
    day = "day"
    week = "week"
    month = "month"
    year = "year"


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
