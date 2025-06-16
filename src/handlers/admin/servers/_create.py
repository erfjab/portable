from eiogram import Router
from eiogram.types import CallbackQuery, Message
from eiogram.stats import State, StatsGroup, StatsManager
from eiogram.filters import StatsFilter, Text

from src.keys.admin import AdminCB, AdminKB, SectionType, ActionType
from src.db import Session, Server, User
from src.language import MesText
from src.utils.exceptions import (
    DuplicateError,
    PatternValidationError,
    ResourceNotFoundError,
)
from src.clients import ClientManager

router = Router()


class ServerCreateForm(StatsGroup):
    REMARK = State()
    # TYPE = State()
    CONFIG = State()


@router.callback_query(
    AdminCB.filter(section=SectionType.SERVER, action=ActionType.CREATE, target=None)
)
async def servers_create(
    callback_query: CallbackQuery, db: Session, stats: StatsManager
):
    await stats.set_state(ServerCreateForm.REMARK)
    return await callback_query.message.edit(
        text=MesText.ENTER_REMARK,
        reply_markup=AdminKB.servers_cancel(),
    )


@router.message(StatsFilter(ServerCreateForm.REMARK), Text())
async def remark_handler(message: Message, stats: StatsManager, db: Session):
    if Server.get_by_remark(db, message.text):
        raise DuplicateError()
    await stats.upsert_data(remark=message.text)
    await stats.clear_stats()
    update = await message.answer(
        text=MesText.SELECT_TYPE,
        reply_markup=AdminKB.servers_types(),
    )
    return User.clear_messages(db, update)


@router.callback_query(
    AdminCB.filter(section=SectionType.SERVER, action=ActionType.CREATE, target=...)
)
async def type_handler(
    callback_query: CallbackQuery,
    callback_data: AdminCB,
    stats: StatsManager,
):
    await stats.upsert_data(target_type=callback_data.target)
    await stats.set_state(ServerCreateForm.CONFIG)
    return await callback_query.message.edit(
        text=MesText.ENTER_SERVER_CONFIG,
        reply_markup=AdminKB.servers_cancel(),
    )


@router.message(StatsFilter(ServerCreateForm.CONFIG), Text())
async def config_handler(message: Message, stats: StatsManager, db: Session):
    messages = message.text.split(" ")
    if len(messages) != 3:
        raise PatternValidationError()

    data = await stats.get_data()

    config = {"username": messages[0], "password": messages[1], "host": messages[2]}
    token = await ClientManager.generate_access_token(
        config=config, server_type=data["target_type"]
    )
    if not token:
        raise ResourceNotFoundError()

    Server.create(
        db, remark=data["remark"], type=data["target_type"], config=config, access=token
    )

    await stats.clear_stats()
    update = await message.answer(
        text=MesText.SUCCESS,
        reply_markup=AdminKB.servers_cancel(),
    )
    return User.clear_messages(db, update)
