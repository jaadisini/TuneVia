import re
from typing import Union
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery, Message

from Tune import app
from Tune.utils.database import get_lang, get_served_users, get_served_chats
from Tune.utils.decorators.language import LanguageStart, languageCB
from Tune.utils.inline.help import help_keyboard, help_back_markup, private_help_panel
from Tune.utils.inline.start import private_panel
from config import BANNED_USERS, HELP_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers
from Tune.utils import bot_sys_stats


# ❗ Private help command or "open_help" callback
@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("open_help") & ~BANNED_USERS)
@LanguageStart
async def helper_private(client: Client, update: Union[Message, CallbackQuery], _):
    is_cb = isinstance(update, CallbackQuery)
    language = await get_lang(update.from_user.id)
    _ = get_string(language)

    keyboard = help_keyboard(_, page=0)
    caption = _["help_1"].format(SUPPORT_CHAT)

    if is_cb:
        await update.answer()
        await update.message.edit_caption(caption, reply_markup=keyboard)
    else:
        await update.delete()
        await update.reply_photo(
            photo=HELP_IMG_URL,
            caption=caption,
            reply_markup=keyboard
        )


# ❗ Group command to suggest using private help
@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client: Client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        _["help_2"],
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )


# ✅ Callback from help buttons like "hb1", "hb2", ..., "hb17"
@app.on_callback_query(filters.regex(r"^help_callback hb(\d+)$") & ~BANNED_USERS)
@languageCB
async def help_detail_callback(client: Client, callback_query: CallbackQuery, _):
    btn_id = int(callback_query.matches[0].group(1))
    try:
        text = helpers.get(f"help_{btn_id}")
        if not text:
            return await callback_query.answer("Modul tidak ditemukan.", show_alert=True)
        markup = help_back_markup(_)
        await callback_query.edit_message_caption(
            caption=text,
            reply_markup=markup
        )
    except Exception as e:
        await callback_query.answer(f"Gagal: {e}", show_alert=True)


# ✅ Pagination callback: .Next/Prev
@app.on_callback_query(filters.regex(r"^help_page (\d+)$") & ~BANNED_USERS)
@languageCB
async def paginate_help(client: Client, callback_query: CallbackQuery, _):
    page = int(callback_query.matches[0].group(1))
    markup = help_keyboard(_, page=page)
    await callback_query.answer()
    await callback_query.edit_message_reply_markup(markup)


# ✅ Back to main menu (panel start)
@app.on_callback_query(filters.regex("back_to_main") & ~BANNED_USERS)
@languageCB
async def back_to_main_cb(client: Client, callback_query: CallbackQuery, _):
    out = private_panel(_)
    UP, CPU, RAM, DISK = await bot_sys_stats()
    served_users = len(await get_served_users())
    served_chats = len(await get_served_chats())
    await callback_query.edit_message_caption(
        _["start_2"].format(
            callback_query.from_user.mention,
            app.mention,
            UP, DISK, CPU, RAM, served_users, served_chats
        ),
        reply_markup=InlineKeyboardMarkup(out)
    )
