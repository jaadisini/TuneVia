import asyncio, logging, random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatMemberStatus
from Tune import app, LOGGER

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)
spam_chats = []


@app.on_message(filters.command(["all", "tagall"], prefixes="/") & filters.group)
async def mentionall(client: Client, message: Message):
    chat_id = message.chat.id

    if message.chat.type == "private":
        return await message.reply("__Perintah ini hanya bisa digunakan di grup!__")

    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply("__Hanya admin yang bisa tagall mek!!__")

        if len(message.command) > 1 and message.reply_to_message:
            return await message.reply("__Kata²nya mana mek!!__")
        elif len(message.command) > 1:
            mode = "text_on_cmd"
            msg = message.text.split(None, 1)[1].strip()
        elif message.reply_to_message:
            mode = "text_on_reply"
            msg = message.reply_to_message
            if msg is None:
                return await message.reply("__Tidak bisa mention pesan lama.__")
        else:
            return await message.reply("__Kirim teks atau balas pesan untuk tagall.__")

        if chat_id not in spam_chats:
            spam_chats.append(chat_id)

        emoji = [
            "👍", "👎", "❤", "🔥", "🥰", "😁", "👏", "🤔", "🤯", "😱",
            "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡",
            "🥱", "🥴", "😍", "🐳", "🌚", "💯", "🌭", "🤣", "⚡", "🍌",
            "🏆", "💔", "🤨", "😐", "🍓", "🍾", "😡", "👾", "🤷", "😎",
        ]

        usrnum = 0
        usrtxt = ''
        members = [usr.user.id async for usr in client.get_chat_members(chat_id) if not usr.user.is_bot]

        stop_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚫 Berhenti Tag", callback_data=f"stop_tag:{chat_id}:{message.from_user.id}")],
            [
                InlineKeyboardButton("⏱ 3 Menit", callback_data=f"autostop:{chat_id}:{message.from_user.id}:180"),
                InlineKeyboardButton("⏱ 5 Menit", callback_data=f"autostop:{chat_id}:{message.from_user.id}:300"),
                InlineKeyboardButton("⏱ 10 Menit", callback_data=f"autostop:{chat_id}:{message.from_user.id}:600"),
            ]
        ])

        status_msg = await message.reply(
            f"__Sedang mentag {len(members)} anggota...__", reply_markup=stop_buttons
        )

        for user_id in members:
            if chat_id not in spam_chats:
                break

            try:
                usrnum += 1
                usrtxt += f"[{random.choice(emoji)}](tg://user?id={user_id}) "

                if usrnum == 8:
                    try:
                        if mode == "text_on_cmd":
                            txt = f"<blockquote>{msg}</blockquote>\n\n<blockquote>{usrtxt}</blockquote>\n@ResahBerkata"
                            await client.send_message(chat_id, txt)
                        elif mode == "text_on_reply":
                            await msg.reply(usrtxt)

                        usrnum = 0
                        usrtxt = ''
                        await asyncio.sleep(0.8)

                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                    except Exception as e:
                        LOGGER.error(f"Error kirim pesan: {e}")
                        await asyncio.sleep(0.5)

            except Exception as e:
                LOGGER.error(f"Error memproses pengguna: {e}")

        if usrnum > 0 and chat_id in spam_chats:
            try:
                if mode == "text_on_cmd":
                    txt = f"<blockquote>{msg}</blockquote>\n\n<blockquote>{usrtxt}</blockquote>\n@ResahBerkata"
                    await client.send_message(chat_id, txt)
                elif mode == "text_on_reply":
                    await msg.reply(usrtxt)
            except Exception as e:
                LOGGER.error(f"Error akhir: {e}")

        await status_msg.edit("__Mention selesai.__")

    except Exception as e:
        LOGGER.error(f"Error dalam tagall: {e}")
    finally:
        if chat_id in spam_chats:
            spam_chats.remove(chat_id)


@app.on_callback_query(filters.regex(r"stop_tag:(-?\d+):(\d+)"))
async def stop_tag_callback(client: Client, callback_query):
    chat_id, user_id = map(int, callback_query.data.split(":")[1:])
    from_user = callback_query.from_user.id

    if from_user != user_id:
        return await callback_query.answer("⛔ Bukan kamu yang mulai tag ini!", show_alert=True)

    if chat_id in spam_chats:
        spam_chats.remove(chat_id)
        await callback_query.edit_message_text("✅ Proses tag dihentikan oleh admin.")
    else:
        await callback_query.answer("❌ Tidak ada tag aktif.", show_alert=True)


@app.on_callback_query(filters.regex(r"autostop:(-?\d+):(\d+):(\d+)"))
async def auto_stop_tag(client: Client, callback_query):
    chat_id, user_id, seconds = map(int, callback_query.data.split(":")[1:])
    from_user = callback_query.from_user.id

    if from_user != user_id:
        return await callback_query.answer("⛔ Bukan kamu yang mulai tag ini!", show_alert=True)

    await callback_query.answer(f"✅ Proses tag akan berhenti otomatis dalam {seconds // 60} menit.")
    await asyncio.sleep(seconds)

    if chat_id in spam_chats:
        spam_chats.remove(chat_id)
        try:
            await callback_query.message.edit_text(f"⏹ Proses tag otomatis dihentikan setelah {seconds // 60} menit.")
        except:
            pass


@app.on_message(filters.command(["cancel"], prefixes="/") & filters.group)
async def cancel_spam(client: Client, message: Message):
    chat_id = message.chat.id
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply("__Hanya admin yang bisa cancel ya babi!__")

    if chat_id not in spam_chats:
        return await message.reply("__Ga ada tagall ngapain cansel asu!...__")

    try:
        spam_chats.remove(chat_id)
    except:
        pass
    return await message.reply("__Oke aku diem.__")


def load():
    LOGGER.info("Modul TagAll berhasil dimuat")


__MODULE__ = "Tᴀɢᴀʟʟ"
__HELP__ = """
/all | /tagall [pesan] atau reply ke pesan — Tag semua member grup
/cancel — Hentikan proses tagall
Tombol "Berhenti Tag" — Hentikan secara manual
Tombol Otomatis — Hentikan setelah 3, 5, atau 10 menit
"""
