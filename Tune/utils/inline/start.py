from pyrogram.types import InlineKeyboardButton
import config
from Tune import app


def start_panel(_):
    return [[InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHANNEL)]]


def private_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_3"], callback_data="open_help"),
        ],
        [
            InlineKeyboardButton(text= "Donasi", url=f"https://files.catbox.moe/u0uns0.jpg"),
        ],
         [
            InlineKeyboardButton(text= "Store", url=f"https://t.me/NakamaMarket"),
        ],
    ]
