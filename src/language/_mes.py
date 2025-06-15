from enum import StrEnum


class MesText(StrEnum):
    START = "<b>👋🏻 Hi Dear <code>{full_name}</code></b>"
    SERVERS_MENU = "<b>📡 Server management menu</b>"
    SERVERS_INFO = (
        "<b>Remark:</b> <code>{remark}</code>\n"
        "<b>Enable:</b> <code>{enable}</code>\n"
        "<b>Type:</b> <code>{type}</code>\n"
        "<b>Config:</b>\n<pre>{config}</pre>\n"
    )
    ENTER_REMARK = "📝 Enter a remark [name]:\n💡 Master, test..."
    SELECT_TYPE = "🪖 Select a type:"
    ENTER_SERVER_CONFIG = (
        "🗃 Enter server config [panel]:\n"
        "- Username\n"
        "- Password\n"
        "- Host (https://sub.domain.com:port)\n"
        "💡 Erfan Sfw74sd https://panel.erfjab.top:80"
    )
    SUCCESS = "✅ Successfully"
    FAILED = "❌ Unsuccessful"
    FORGET = "Ok..."
    APPROVAL = "❔ Are you sure?"
    ERROR_PATTERN: str = "⚠️ Please enter the text according to the defined pattern."
    ERROR_DUPLICATE: str = "⚠️ Duplicate entry, please enter a unique item."
    ERROR_UNAVAILABLE: str = "⚠️ Service is currently unavailable."
    ERROR_INTEGER: str = "⚠️ Your input must be a number."
    ERROR_NOT_FOUND: str = "⚠️ The requested item was not found."
    SUBCRIPTIONS_MENU = "<b>👤 Subscriptions management menu</b>"
    SUBSCRIPTIONS_INFO = (
        "<b>Remark:</b> <code>{remark}</code>\n"
        "<b>Key:</b> <code>{key}</code>\n"
        "<b>Link:</b> <code>{link}</code>\n"
    )
