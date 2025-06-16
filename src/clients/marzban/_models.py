from enum import Enum
from typing import Optional, Dict, List
from pydantic import BaseModel


class MarzbanToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MarzbanUserStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    LIMITED = "limited"
    EXPIRED = "expired"
    ONHOLD = "on_hold"


class MarzbanAdmin(BaseModel):
    username: str
    is_sudo: bool


class MarzbanUserResponse(BaseModel):
    username: Optional[str] = None
    proxies: Optional[Dict[str, dict]] = {}
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    inbounds: Optional[Dict[str, List[str]]] = None
    on_hold_expire_duration: Optional[int] = None
    status: MarzbanUserStatus = MarzbanUserStatus.ACTIVE
    used_traffic: Optional[int] = None
    subscription_url: Optional[str] = None
    admin: Optional[MarzbanAdmin] = None

    @property
    def data_left(self) -> int:
        if not self.data_limit:
            return 0
        if not self.used_traffic:
            return self.data_limit
        return self.data_limit - self.used_traffic


class MarzbanProxyTypes(str, Enum):
    VMess = "vmess"
    VLESS = "vless"
    Trojan = "trojan"
    Shadowsocks = "shadowsocks"


class MarzbanProxyInbound(BaseModel):
    tag: str
    protocol: MarzbanProxyTypes
