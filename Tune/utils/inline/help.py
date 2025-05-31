from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from Tune import app  # ganti sesuai nama Client-mu jika bukan "app"

# Jumlah item per halaman
ITEMS_PER_PAGE = 6

# Fungsi utama untuk membuat menu help dengan halaman
def help_keyboard_page(page, _):
    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    buttons = []

    for i in range(start_index + 1, min(end_index + 1, 16)):  # total 15 tombol
        if (i - 1 - start_index) % 3 == 0:
            buttons.append([])
        buttons[-1].append(
            InlineKeyboardButton(
                text=_[f"H_B_{i}"],
                callback_data=f"help_callback hb{i}"
            )
        )

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton("Sebelumnya", callback_data=f"help_page {page - 1}")
        )
    if end_index < 15:
        nav_buttons.append(
            InlineKeyboardButton("Selanjutnya", callback_data=f"help_page {page + 1}")
        )
    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append(
        [
            InlineKeyboardButton(text="ᴍᴇɴᴜ", callback_data="back_to_main"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ]
    )

    return InlineKeyboardMarkup(buttons)

# Fungsi markup tombol kembali
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

# Panel bantuan jika dari /start di PM
def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_8"],
                url=f"https://t.me/{app.username}?start=help"
            )
        ]
    ]


# Callback handler help_page (navigasi halaman)
@app.on_callback_query(filters.regex(r"^help_page (\d+)"))
async def help_page_callback(_, query: CallbackQuery):
    page = int(query.data.split()[1])
    _lang = await get_lang(query.message.chat.id)  # Anda harus menyesuaikan fungsi ini
    await query.message.edit_reply_markup(
        reply_markup=help_keyboard_page(page, _lang)
    )


# Contoh callback jika ingin buka halaman detail bantuan
@app.on_callback_query(filters.regex(r"^help_callback hb(\d+)"))
async def help_callback_detail(_, query: CallbackQuery):
    hb_index = query.data.split()[1]
    _lang = await get_lang(query.message.chat.id)
    await query.message.edit_text(
        text=f"Detail bantuan untuk modul {_lang.get(f'H_B_{hb_index[-1]}', 'Tidak ditemukan.')}",
        reply_markup=help_back_markup(_lang)
    )


# Dummy get_lang (ganti sesuai sistemmu)
async def get_lang(chat_id):
    # Ganti ini dengan fetch bahasa asli dari DB kamu
    return {
        "H_B_1": "Admin",
        "H_B_2": "Otorisasi",
        "H_B_3": "Gcast",
        "H_B_4": "Blokir Obrolan",
        "H_B_5": "Blokir Pengguna",
        "H_B_6": "Mainkan Saluran",
        "H_B_7": "Global Ban",
        "H_B_8": "Ulangi",
        "H_B_9": "Log",
        "H_B_10": "Ping",
        "H_B_11": "Mainkan",
        "H_B_12": "Acak",
        "H_B_13": "Cari",
        "H_B_14": "Lagu",
        "H_B_15": "Kecepatan",
        "H_B_16": "Tag All",
        "H_B_17": "Anti Gcast"
        "S_B_8": "Klik untuk bantuan",
        "BACK_BUTTON": "Kembali",
        "CLOSE_BUTTON": "Tutup"
    }
