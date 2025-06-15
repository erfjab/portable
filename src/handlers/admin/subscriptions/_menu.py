from eiogram import Router
from eiogram.types import CallbackQuery
from src.keys.admin import AdminCB, AdminKB, SectionType, ActionType
from src.db import Session, Subscription
from src.language import MesText

router = Router()


@router.callback_query(
    AdminCB.filter(section=SectionType.SUBCRIPTION, action=ActionType.MENU)
)
async def subscriptions_menu(callback_query: CallbackQuery, db: Session):
    subscriptions = Subscription.get_all(db)
    return await callback_query.message.edit(
        text=MesText.SUBCRIPTIONS_MENU,
        reply_markup=AdminKB.subscriptions_menu(subscriptions=subscriptions),
    )
