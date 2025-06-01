from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Tune import app

# Jumlah tombol per halaman
BUTTONS_PER_PAGE = 6

def help_keyboard(_, page=0):
    total_buttons = 17
    total_pages = (total_buttons + BUTTONS_PER_PAGE - 1) // BUTTONS_PER_PAGE
    page = max(0, min(page, total_pages - 1))  # Jaga agar page tidak out of range

    start = page * BUTTONS_PER_PAGE + 1
    end = min(start + BUTTONS_PER_PAGE, total_buttons + 1)

    buttons = []
    for i in range(start, end):
        if (i - start) % 3 == 0:
            buttons.append([])  # Baris baru setiap 3 tombol
        buttons[-1].append(
            InlineKeyboardButton(
                text=_[f"H_B_{i}"],
                callback_data=f"help_callback hb{i}"
            )
        )

    # Tombol Navigasi: Prev / Next
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton("sebelumnya", callback_data=f"help_page {page - 1}")
        )
    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton("selanjutnya", callback_data=f"help_page {page + 1}")
        )
    if nav_buttons:
        buttons.append(nav_buttons)

    # Baris terakhir: Menu & Close
    buttons.append([
        InlineKeyboardButton(text="ᴍᴇɴᴜ", callback_data="back_to_main"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
    ])

    return InlineKeyboardMarkup(buttons)

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

@Client.on_callback_query(filters.regex(r"^help_page (\d+)$"))
async def paginate_help_menu(client, callback_query: CallbackQuery):
    page = int(callback_query.matches[0].group(1))
    markup = help_keyboard(_, page=page)  # Ganti `_` dengan fungsi translate kamu
    await callback_query.edit_message_reply_markup(markup)


def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],  # Contoh: "Klik di sini untuk bantuan"
                url=f"https://t.me/{app.username}?start=help"
            )
        ]
    ]
    
def help_back_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],  # Contoh: "🔙 Kembali"
                    callback_data="open_help"
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],  # Contoh: "❌ Tutup"
                    callback_data="close"
                )
            ]
        ]
    )

