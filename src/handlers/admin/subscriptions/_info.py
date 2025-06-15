from eiogram import Router
from eiogram.types import CallbackQuery

from src.keys.admin import AdminCB, AdminKB, SectionType, ActionType
from src.db import Session, Subscription
from src.language import MesText
from src.utils import ResourceNotFoundError


router = Router()


@router.callback_query(
    AdminCB.filter(section=SectionType.SUBCRIPTION, action=ActionType.INFO)
)
async def subscription_info(
    callback_query: CallbackQuery, callback_data: AdminCB, db: Session
):
    subscription = Subscription.get_by_id(db, int(callback_data.target))
    if not subscription:
        raise ResourceNotFoundError()
    return await callback_query.message.edit(
        text=MesText.SUBSCRIPTIONS_INFO.format(**subscription.format()),
        reply_markup=AdminKB.subscriptions_cancel(),
    )
