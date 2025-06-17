from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.stats import StatsManager
from src.keys.admin import AdminCB, AdminKB, SectionType, ActionType, OperationType
from src.db import Session, Server, ServerType
from src.language import MesText
from src.utils.exceptions import ServiceUnavailableError
from src.utils.transfer import SubscriptionTransfer

router = Router()


@router.callback_query(
    AdminCB.filter(
        section=SectionType.SUBCRIPTION,
        action=ActionType.OPERATION,
        target=None,
        command=OperationType.TRANSFER_SUB,
    )
)
async def subscriptions_operation(callback_query: CallbackQuery, db: Session):
    servers = Server.get_all(db, enable=True, type=ServerType.MARZNESHIN)
    if not servers or len(servers) < 1:
        raise ServiceUnavailableError()
    return await callback_query.message.edit(
        text=MesText.SUBSCRIPTIONS_TRANSFER_SUB_FROM,
        reply_markup=AdminKB.subscriptions_transfer_servers(
            servers=servers, command=OperationType.TRANSFER_SUB_FROM
        ),
    )


@router.callback_query(
    AdminCB.filter(
        section=SectionType.SUBCRIPTION,
        action=ActionType.OPERATION,
        target=...,
        command=OperationType.TRANSFER_SUB_FROM,
    )
)
async def transfer_from(
    callback_query: CallbackQuery,
    callback_data: AdminCB,
    db: Session,
    stats: StatsManager,
):
    servers = Server.get_all(db, enable=True, type=ServerType.MARZBAN)
    if not servers or len(servers) < 1:
        raise ServiceUnavailableError()
    servers = [server for server in servers if server.id != int(callback_data.target)]
    await stats.upsert_data(from_server=callback_data.target)
    return await callback_query.message.edit(
        text=MesText.SUBSCRIPTIONS_TRANSFER_SUB_TO,
        reply_markup=AdminKB.subscriptions_transfer_servers(
            servers=servers, command=OperationType.TRANSFER_SUB_TO
        ),
    )


@router.callback_query(
    AdminCB.filter(
        section=SectionType.SUBCRIPTION,
        action=ActionType.OPERATION,
        target=...,
        command=OperationType.TRANSFER_SUB_TO,
    )
)
async def transfer_to(
    callback_query: CallbackQuery,
    callback_data: AdminCB,
    db: Session,
    stats: StatsManager,
):
    await callback_query.message.edit(text=MesText.WAIT)
    data = await stats.get_data()
    from_server = Server.get_by_id(db, int(data["from_server"]))
    to_server = Server.get_by_id(db, int(callback_data.target))
    exports = await SubscriptionTransfer.exports(
        db, from_server=from_server, to_server=to_server
    )
    imports = await SubscriptionTransfer.imports(
        server=to_server, subscriptions=exports
    )
    return await callback_query.message.edit(
        text=MesText.SUBSCRIPTIONS_TRANSFER_RESULT.format(**imports),
        reply_markup=AdminKB.subscriptions_cancel(),
    )
