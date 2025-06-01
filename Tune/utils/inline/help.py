from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Tune import app

def help_keyboard(_):
    buttons = []
    for i in range(1, 18):  # Dari H_B_1 sampai H_B_17
        if (i - 1) % 3 == 0:
            buttons.append([])  # Baris baru setiap 3 tombol
        buttons[-1].append(
            InlineKeyboardButton(
                text=_[f"H_B_{i}"],
                callback_data=f"help_callback hb{i}"
            )
        )
    
    # Tambahkan baris terakhir untuk MENU & CLOSE
    buttons.append(
        [
            InlineKeyboardButton(
                text="ᴍᴇɴᴜ", 
                callback_data="back_to_main"
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close"
            )
        ]
    )

    return InlineKeyboardMarkup(buttons)


def help_back_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="open_help"
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close"
                ),
            ]
        ]
    )


def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?start=help"
            )
        ]
    ]
