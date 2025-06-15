from eiogram import Router
from eiogram.types import Message, CallbackQuery
from eiogram.filters import Command
from src.db import User, Session
from src.language import MesText
from src.keys.admin import AdminKB, SectionType, ActionType, AdminCB

router = Router()


@router.message(Command("start"))
async def start(message: Message, db: Session, dbuser: User):
    update = await message.answer(
        text=MesText.START.format(**dbuser.format()), reply_markup=AdminKB.home()
    )
    return User.clear_messages(db, update)


@router.callback_query(AdminCB.filter(section=SectionType.HOME, action=ActionType.MENU))
async def home(callback_query: CallbackQuery, db: Session, dbuser: User):
    update = await callback_query.message.answer(
        text=MesText.START.format(**dbuser.format()), reply_markup=AdminKB.home()
    )
    return User.clear_messages(db, update)
