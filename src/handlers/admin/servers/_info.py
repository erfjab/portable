from eiogram import Router
from eiogram.types import CallbackQuery

from src.keys.admin import AdminCB, AdminKB, SectionType, ActionType
from src.db import Session, Server
from src.language import MesText
from src.utils.exceptions import ResourceNotFoundError


router = Router()


@router.callback_query(
    AdminCB.filter(section=SectionType.SERVER, action=ActionType.INFO)
)
async def servers_info(
    callback_query: CallbackQuery, callback_data: AdminCB, db: Session
):
    server = Server.get_by_id(db, int(callback_data.target))
    if not server:
        raise ResourceNotFoundError()
    return await callback_query.message.edit(
        text=MesText.SERVERS_INFO.format(**server.format()),
        reply_markup=AdminKB.servers_update(server=server),
    )
