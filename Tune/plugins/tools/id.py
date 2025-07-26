import os

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from Tune import app

# Simpan status per chat_id
chatbot_enabled = {}

# Fungsi baca respon.txt
def load_responses():
    responses = {}
    if not os.path.exists("respon.txt"):
        return responses
    with open("respon.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                responses[key.lower()] = val.strip()
    return responses

RESPONSES = load_responses()

# 📌 Command ID
@app.on_message(filters.command("id"))
async def get_id(client, message: Message):
    chat, user, reply = message.chat, message.from_user, message.reply_to_message
    out = []

    if message.link:
        out.append(f"**[ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message.id}`")
    else:
        out.append(f"**ᴍᴇssᴀɢᴇ ɪᴅ:** `{message.id}`")

    out.append(f"**[ʏᴏᴜʀ ɪᴅ:](tg://user?id={user.id})** `{user.id}`")

    if len(message.command) == 2:
        try:
            target = message.text.split(maxsplit=1)[1]
            tgt_user = await client.get_users(target)
            out.append(f"**[ᴜsᴇʀ ɪᴅ:](tg://user?id={tgt_user.id})** `{tgt_user.id}`")
        except Exception:
            return await message.reply_text("**ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ.**", quote=True)

    if chat.username and chat.type != "private":
        out.append(f"**[ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`")
    else:
        out.append(f"**ᴄʜᴀᴛ ɪᴅ:** `{chat.id}`")

    if reply:
        if reply.link:
            out.append(f"**[ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.id}`")
        else:
            out.append(f"**ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:** `{reply.id}`")

        if reply.from_user:
            out.append(f"**[ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`")

        if reply.forward_from_chat:
            out.append(f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ **{reply.forward_from_chat.title}** ʜᴀs ɪᴅ `{reply.forward_from_chat.id}`")

        if reply.sender_chat:
            out.append(f"ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ: `{reply.sender_chat.id}`")

    await message.reply_text(
        "\n".join(out),
        disable_web_page_preview=True,
        parse_mode=ParseMode.MARKDOWN
    )

# 📌 Aktif/nonaktifkan fitur AutoReply
@app.on_message(filters.command("autoreply"))
async def toggle_autoreply(client, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        status = chatbot_enabled.get(chat_id, False)
        return await message.reply_text(f"AutoReply saat ini: {'Aktif' if status else 'Nonaktif'}")
    
    cmd = message.command[1].lower()
    if cmd == "on":
        chatbot_enabled[chat_id] = True
        await message.reply_text("✅ AutoReply diaktifkan untuk chat ini.")
    elif cmd == "off":
        chatbot_enabled[chat_id] = False
        await message.reply_text("❌ AutoReply dinonaktifkan untuk chat ini.")
    else:
        await message.reply_text("Gunakan: `/autoreply on` atau `/autoreply off`", parse_mode=ParseMode.MARKDOWN)

# 📌 Auto balasan
@app.on_message(filters.text & ~filters.command(["autoreply"]))
async def auto_reply_handler(client, message: Message):
    chat_id = message.chat.id
    if not chatbot_enabled.get(chat_id, False):
        return

    text = message.text.lower()
    for keyword, response in RESPONSES.items():
        if keyword in text:
            await message.reply_text(response)
            break
