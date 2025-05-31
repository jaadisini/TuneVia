import re
from typing import Union
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, Message, CallbackQuery

from Tune import app
from config import BANNED_USERS, HELP_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers
from Tune.utils import bot_sys_stats
from Tune.utils.database import get_lang, get_served_users, get_served_chats
from Tune.utils.decorators.language import LanguageStart, languageCB
from Tune.utils.inline.help import help_keyboard_page, help_back_markup, private_help_panel
from Tune.utils.inline.start import private_panel


# PM: /help command
@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("open_help") & ~BANNED_USERS)
@LanguageStart
async def helper_private(client: Client, update: Union[Message, CallbackQuery], _):
    is_cb = isinstance(update, CallbackQuery)
    lang = await get_lang(update.from_user.id)
    __ = get_string(lang)
    keyboard = help_keyboard_page(1, __)
    caption = __["help_1"].format(SUPPORT_CHAT)

    if is_cb:
        await update.answer()
        await update.message.edit_caption(
            caption,
            reply_markup=keyboard
        )
    else:
        await update.reply_photo(
            photo=HELP_IMG_URL,
            caption=caption,
            reply_markup=keyboard
        )


# Grup: /help reply PM panel
@app.on_message(filters.command(["help"]) & filter_
