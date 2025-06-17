from typing import Union, Optional
from enum import StrEnum
from eiogram.utils.callback_data import CallbackData


class SectionType(StrEnum):
    HOME = "hm"
    SETTING = "st"
    SERVER = "sv"
    SUBCRIPTION = "sp"


class ActionType(StrEnum):
    MENU = "mn"
    UPDATE = "up"
    SELECT = "sl"
    INFO = "nf"
    CREATE = "cr"
    OPERATION = "op"


class UpdateType(StrEnum):
    REMARK = "mr"
    ENABLE = "nb"
    DISABLE = "ds"
    SERVER_CONFIG = "sc"
    REMOVE = "rm"


class OperationType(StrEnum):
    TRANSFER_SUB = "ts"
    TRANSFER_SUB_FROM = "tf"
    TRANSFER_SUB_TO = "tt"


class AdminCB(CallbackData, prefix="a"):
    section: SectionType = SectionType.HOME
    action: ActionType = ActionType.MENU
    target: Optional[Union[str, int]] = None
    command: Optional[Union[str, StrEnum]] = None
    approval: Optional[bool] = None
