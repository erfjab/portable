from typing import Optional, Union
from eiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from eiogram.utils.inline_builder import InlineKeyboardBuilder
from src.language import KeyText
from src.db import Server, ServerType, Subscription
from ._callback import AdminCB, ActionType, SectionType, UpdateType


class AdminKB:
    @classmethod
    def _add(
        cls,
        kb: InlineKeyboardBuilder,
        *,
        home: bool = True,
        create: Optional[SectionType] = None,
        back: Optional[SectionType] = None,
        target: Optional[Union[str, int]] = None,
    ):
        buttons = []

        if create:
            buttons.append(
                InlineKeyboardButton(
                    text=KeyText.CREATE,
                    callback_data=AdminCB(
                        section=create, action=ActionType.CREATE
                    ).pack(),
                )
            )

        if back:
            buttons.append(
                InlineKeyboardButton(
                    text=KeyText.BACK,
                    callback_data=AdminCB(
                        section=back,
                        action=ActionType.INFO if target else ActionType.MENU,
                        target=target,
                    ).pack(),
                )
            )

        if home:
            buttons.append(
                InlineKeyboardButton(
                    text=KeyText.HOME,
                    callback_data=AdminCB().pack(),
                )
            )

        kb.row(*buttons, size=2)

    @classmethod
    def home(cls) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            text=KeyText.SERVERS,
            callback_data=AdminCB(
                section=SectionType.SERVER, action=ActionType.MENU
            ).pack(),
        )
        kb.add(
            text=KeyText.SUBCRIPTIONS,
            callback_data=AdminCB(
                section=SectionType.SUBCRIPTION, action=ActionType.MENU
            ).pack(),
        )
        kb.adjust(2)
        return kb.as_markup()

    @classmethod
    def servers_menu(cls, servers: list[Server]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for server in servers:
            kb.add(
                text=server.kb_remark,
                callback_data=AdminCB(
                    section=SectionType.SERVER, action=ActionType.INFO, target=server.id
                ).pack(),
            )
        kb.adjust(2)
        cls._add(kb, back=SectionType.SERVER, create=SectionType.SERVER)
        return kb.as_markup()

    @classmethod
    def servers_update(cls, server: Server) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        updates = [
            UpdateType.DISABLE if server.enable else UpdateType.ENABLE,
            UpdateType.REMARK,
            UpdateType.REMOVE,
            UpdateType.SERVER_CONFIG,
        ]
        for update in updates:
            kb.add(
                text=KeyText.update_key(update),
                callback_data=AdminCB(
                    section=SectionType.SERVER,
                    action=ActionType.UPDATE,
                    target=server.id,
                    command=update,
                ).pack(),
            )
        kb.adjust(2, 2, 2)
        cls._add(kb, back=SectionType.SERVER)
        return kb.as_markup()

    @classmethod
    def servers_cancel(cls) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        cls._add(kb, back=SectionType.SERVER)
        return kb.as_markup()

    @classmethod
    def servers_types(cls) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for server in [ServerType.MARZBAN, ServerType.MARZNESHIN]:
            kb.add(
                text=server,
                callback_data=AdminCB(
                    section=SectionType.SERVER,
                    action=ActionType.CREATE,
                    target=server,
                ).pack(),
            )
        kb.adjust(1)
        cls._add(kb, back=SectionType.SERVER)
        return kb.as_markup()

    @classmethod
    def approval(cls, section: SectionType) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            text=KeyText.YES,
            callback_data=AdminCB(
                section=section, action=ActionType.UPDATE, approval=True
            ).pack(),
        )
        kb.add(
            text=KeyText.NO,
            callback_data=AdminCB(
                section=section, action=ActionType.UPDATE, approval=False
            ).pack(),
        )
        kb.adjust(2)
        cls._add(kb, back=SectionType.SERVER)
        return kb.as_markup()

    @classmethod
    def subscriptions_menu(
        cls, subscriptions: list[Subscription]
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for subscription in subscriptions:
            kb.add(
                text=subscription.kb_remark,
                callback_data=AdminCB(
                    section=SectionType.SUBCRIPTION,
                    action=ActionType.INFO,
                    target=subscription.id,
                ).pack(),
            )
        kb.adjust(2)
        cls._add(kb)
        return kb.as_markup()

    @classmethod
    def subscriptions_cancel(cls) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        cls._add(kb, back=SectionType.SUBCRIPTION)
        return kb.as_markup()
