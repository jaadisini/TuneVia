import asyncio
import json

from Tune import app
import re
import os
from pyrogram import *
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, MessageDeleteForbidden, UserNotParticipant

from config import *
from pyrogram.enums import ChatMemberStatus
from motor.motor_asyncio import AsyncIOMotorClient  # Import the correct class

# Instantiate the MongoDB client
mongo_client = AsyncIOMotorClient(MONGO_DB_URI)  # Ensure MongoCli is correctly instantiated
db = mongo_client["DOR"]
user_collection = db["user_dia"]
gc = db["listgrup"]
psnz = db["msg_text"]
whitelist = db["white_dia"]

import asyncio
from pyrogram import filters, enums
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

STATUS = enums.ChatMemberStatus

async def isMember(filter, client, update):
    try:
        member = await client.get_chat_member(chat_id=update.chat.id, user_id=update.from_user.id)
    except FloodWait as wait_err:
        await asyncio.sleep(wait_err.value)
    except UserNotParticipant:
        return False
    except:
        return False

    return member.status not in [STATUS.OWNER, STATUS.ADMINISTRATOR]

async def isAdmin(filter, client, update):
    try:
        member = await client.get_chat_member(chat_id=update.chat.id, user_id=update.from_user.id)
    except FloodWait as wait_err:
        await asyncio.sleep(wait_err.value)
    except UserNotParticipant:
        return False
    except:
        return False

    return member.status in [STATUS.OWNER, STATUS.ADMINISTRATOR]

Member = filters.create(isMember)
Admin = filters.create(isAdmin)

def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])
        


async def get_user_ids(client_id):
    user_ids = await user_collection.find_one({"_id": client_id})
    return user_ids["user_dia"] if user_ids else []

async def get_white_ids(client_id):
    white_ids = await whitelist.find_one({"_id": client_id})
    return white_ids["white_dia"] if white_ids else []


async def get_blacklist_status(client_id):
    blacklist_status = await db.settings.find_one({"_id": client_id})
    return blacklist_status["status"] if blacklist_status else False

async def set_blacklist_status(client_id, status):
    await db.settings.update_one({"_id": client_id}, {"$set": {"status": status}}, upsert=True)

async def get_chat_ids(client_id):
    chat_ids = await gc.find_one({"_id": client_id})
    return chat_ids["grup"] if chat_ids else []

async def get_msg_ids(client_id):
    msg_ids = await psnz.find_one({"_id": client_id})
    return msg_ids["msg_text"] if msg_ids else []

async def purge(message):
    await asyncio.sleep(0.5)
    await message.delete()

def get_message(message):
    msg = (
        message.reply_to_message
        if message.reply_to_message
        else "" if len(message.command) < 2 else " ".join(message.command[1:])
    )
    return msg


CONFIG_FILE = "config.json"

async def autoend_off():
    chat_id = 123
    autoend[chat_id] = False
    user = await autoenddb.find_one({"chat_id": chat_id})
    if user:
        return await autoenddb.delete_one({"chat_id": chat_id})

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

config = load_config()



    

def emoji(alias):
    emojis = {
        "bintang": "<emoji id=5931592939514892319>⭐</emoji>",
        "loading": "<emoji id=5801044672658805468>✨</emoji>",
        "proses": "<emoji id=6276248783525251352>🔄</emoji>",
        "gagal": "<emoji id=6278161560095426411>❌</emoji>",
        "done": "<emoji id=5852871561983299073>✅</emoji>",
        "upload": "<emoji id=5911100572508885928>♻️</emoji>",
        "roses": "<emoji id=5341312820698948923>⚠️</emoji>",
        "selesai": "<emoji id=5341576484446283436>‼️</emoji>",
        "on": "<emoji id=6275808772715710450>🎚️</emoji>",
        "off": "<emoji id=6276295366740543459>⛔</emoji>",
        "daftar": "<emoji id=5974045315391556490>📝</emoji>",
    }
    return emojis.get(alias, "Emoji tidak ditemukan.")

Q = emoji("bintang")
gagal = emoji("gagal")
prs = emoji("proses")
batal = emoji("gagal")
rs = emoji("roses")
sls = emoji("selesai")
dn = emoji("done")
on = emoji("on")
off = emoji("off")
dftr = emoji("daftar")


async def isGcast(filter, client, update):
    bl = "€¥£¢𝑎𝑏𝑐𝑑𝑒𝑓𝑔𝒉𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ×̰͓̰̈́̈́̈́̈́ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿 🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿 ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴛᴜᴠᴡʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴛᴜᴠᴡʏᴢᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴛᴜᴠᴡʏᴢᗩᗷᑕᗞᗴᖴᏀᕼᏆᒍᏦしᗰᑎᝪᑭᑫᖇᔑᎢᑌᐯᗯ᙭ᎩᏃᗩᗷᑕᗞᗴᖴᏀᕼᏆᒍᏦしᗰᑎᝪᑭᑫᖇᔑᎢᑌᐯᗯ᙭ᎩᏃᎪᏴᏟᎠᎬҒᏀᎻᏆᎫᏦᏞᎷΝϴᏢϘᎡՏͲႮᏙᏔХᎽᏃᎪᏴᏟᎠᎬҒᏀᎻᏆᎫᏦᏞᎷΝϴᏢϘᎡՏͲႮᏙᏔХᎽᏃａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
    awoos = update.text
    x = awoos.lower()
    xx = await get_msg_ids(client.me.id)
        
    with open('bl.txt', 'r') as file:
        blc = [w.lower().strip() for w in file.readlines()]
        for chara in bl:
            blc.append(chara)

    for chara in blc:
        if chara in x:
            return True
        
    if x in xx:
        return True
    
    kont = update.from_user.id
    meki = await get_user_ids(client.me.id)

    if kont in meki:
        return True
        
    return False

Gcast = filters.create(isGcast)



        

@app.on_message(filters.command("dor",["","/"]) & ~filters.private & Admin)
async def add_user_to_blacklist(c, m):
    if len(m.command) != 2 and not m.reply_to_message:
        await m.reply_text(
            f"{batal}**gunakan format** : `duar` **user id atau balas ke pesan untuk menambahkan ke daftar antigcast {Q}**",
            quote=True,
        )
        return

    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
    else:
        try:
            user_id = int(m.command[1])
        except ValueError:
            try:
                user = await c.get_users(m.command[1])
                user_id = user.id
            except Exception:
                await m.reply_text(f"{gagal} Tidak dapat menemukan pengguna dengan username {m.command[1]}", quote=True)
                return

    user_ids = await get_user_ids(c.me.id)
    if user_id not in user_ids:
        user_ids.append(user_id)
        await user_collection.update_one({"_id": c.me.id}, {"$set": {"user_dia": user_ids}}, upsert=True)
        x = await m.reply_text(f"{Q}**user dengan id** `{user_id}` **telah ditambahkan ke daftar antigcast** {dn}", quote=True)
        await x.delete()
    else:
        await m.reply_text(f"{dn}**user tersebut sudah ada dalam daftar antigcast {Q}**", quote=True)
        await m.delete()
    
@app.on_message(filters.command("listdor") & ~filters.private & Admin)
async def display_blacklist(client, message):
    user_ids = await get_user_ids(client.me.id)
    await message.reply_text(f"{dftr} ini hasilnya : `{user_ids}`\n", quote=True)

@app.on_message(filters.command("undor",["","/"]) & ~filters.private & Admin)
async def remove_user_from_blacklist(c, m):
    if len(m.command) != 2 and not m.reply_to_message:
        await m.reply_text(
            f"{batal}**gunakan format** : `unduar` **user id atau balas ke pesan untuk menghapus dari daftar antigcast {Q}**",
            quote=True,
        )
        return

    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
    else:
        user_id = int(m.command[1])

    user_ids = await get_user_ids(c.me.id)
    if user_id in user_ids:
        user_ids.remove(user_id)
        await user_collection.update_one({"_id": c.me.id}, {"$set": {"user_dia": user_ids}}, upsert=True)
        await m.reply_text(f"{Q}**user dengan id** `{user_id}` **telah dihapus dalam daftar antigcast** {dn}", quote=True)
    else:
        await m.reply_text(f"{Q}**user tersebut tidak ada dalam daftar antigcast {gagal}**", quote=True)

@app.on_message(filters.command("liat") & ~filters.private)
async def checkstatus(client, message):
    cek = await get_blacklist_status(client.me.id)
    if cek:
        await message.reply_text(f"{Q}**anda sudah mengaktifkan antigcast**{dn}", quote=True)
    else:
        await message.reply_text(f"{Q}**anda belum mengaktifkan antigcast**{gagal}", quote=True)


@app.on_message(filters.command("bl",["","/"]) & ~filters.private & Admin)
async def add_pesan(c, m):
    _rply = get_arg(m)
    if m.reply_to_message:
        _rply = m.reply_to_message.text or m.reply_to_message.caption
    if not _rply:
        x = await m.reply(f"mohon balas ke pengguna atau masukan pesan")
        await x.delete()
        return
    user_text = _rply
    msg_ids = await get_msg_ids(c.me.id)
    if user_text not in msg_ids:
        msg_ids.append(user_text)
        await psnz.update_one({"_id": c.me.id}, {"$set": {"msg_text": msg_ids}}, upsert=True)
        sukses = await m.reply_text(f"<blockquote><b>{user_text} berhasil di tambahkan ke database{dn}</b></blockquote>", quote=True)
        await purge(m)
        await sukses.delete()
    else:
        x = await m.reply_text(f"pesan sudah ada di dalam database{gagal}", quote=True)
        await asyncio.sleep(0.5)
        await x.delete()

@app.on_message(filters.command("cekbl") & ~filters.private)
async def strdb(client, message):
    pesan = await get_msg_ids(client.me.id)
    try:
        await message.reply_text(pesan)
    except MessageTooLong:
        with open("db.txt", "a", encoding="utf-8") as file:
            file.write(f"{pesan}\n")
        kirim = await message.reply_document(db.txt)
        if kirim:
            os.remove("db.txt")

@app.on_message(filters.command("unbl",["","/"]) & ~filters.private & Admin)
async def remove_kata_from_blacklist(c, m):
    if len(m.command) != 2 and not m.reply_to_message:
        await m.reply_text(
            f"{batal}**gunakan format** : `rmkat` **user id atau balas ke pesan untuk menghapus dari daftar antigcast {Q}**",
            quote=True,
        )
        return

    if m.reply_to_message:
        user_id = m.reply_to_message.text
    else:
        user_id = " ".join(m.command[1:])

    user_ids = await get_msg_ids(c.me.id)
    if user_id in user_ids:
        user_ids.remove(user_id)
        await psnz.update_one({"_id": c.me.id}, {"$set": {"msg_text": user_ids}}, upsert=True)
        await m.reply_text(f"{Q}**berhasil menghapus** `{user_id}` **dari daftar kata antigcast** {dn}", quote=True)
    else:
        await m.reply_text(f"{Q}**kata tersebut tidak ada dalam daftar antigcast {gagal}**", quote=True)


@app.on_message(filters.command("wl",["","/"]) & ~filters.private & Admin)
async def add_user_to_whitelist(c, m):
    if len(m.command) != 2 and not m.reply_to_message:
        await m.reply_text(
            f"{batal}**gunakan format** : `wl` **user id atau balas ke pesan untuk menambahkan ke whitelist antigcast {Q}**",
            quote=True,
        )
        return

    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
    else:
        try:
            user_id = int(m.command[1])
        except ValueError:
            try:
                user = await c.get_users(m.command[1])
                user_id = user.id
            except Exception:
                await m.reply_text(f"{gagal} Tidak dapat menemukan pengguna dengan username {m.command[1]}", quote=True)
                return

    white_ids = await get_white_ids(c.me.id)
    if user_id not in white_ids:
        white_ids.append(user_id)
        await whitelist.update_one({"_id": c.me.id}, {"$set": {"white_dia": white_ids}}, upsert=True)
        await m.reply_text(f"{Q}**user dengan id** `{user_id}` **telah ditambahkan ke whitelist antigcast** {dn}", quote=True)
        await m.delete()
    else:
        await m.reply_text(f"{dn}**user tersebut sudah ada dalam whitelist antigcast {Q}**", quote=True)
        await m.delete()

@app.on_message(filters.command("listwl",["","/"]) & ~filters.private & Admin)
async def display_whitelist(client, message):
    user_ids = await get_white_ids(client.me.id)
    await message.reply_text(f"{dftr} ini hasilnya : `{user_ids}`\n", quote=True)

@app.on_message(filters.command("unwl",["","/"]) & ~filters.private & Admin)
async def remove_user_from_whitelist(c, m):
    if len(m.command) != 2 and not m.reply_to_message:
        await m.reply_text(
            f"{batal}**gunakan format** : `unwl` **user id atau balas ke pesan untuk menghapus dari daftar antigcast {Q}**",
            quote=True,
        )
        return

    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
    else:
        user_id = int(m.command[1])

    white_ids = await get_white_ids(c.me.id)
    if user_id in white_ids:
        white_ids.remove(user_id)
        await whitelist.update_one({"_id": c.me.id}, {"$set": {"white_dia": white_ids}}, upsert=True)
        await m.reply_text(f"{Q}**user dengan id** `{user_id}` **telah dihapus dalam whitelist antigcast** {dn}", quote=True)
        await m.delete()
    else:
        await m.reply_text(f"{Q}**user tersebut tidak ada dalam whitelist antigcast {gagal}**", quote=True)
        await m.delete()


@app.on_message(filters.command("ankes") & ~filters.private & Admin)
async def toggle_antigcast(client, message):
    chat_id = str(message.chat.id)
    user_id = message.from_user.id
    args = message.text.split()
    member = await client.get_chat_member(chat_id, user_id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply("Hanya admin yang dapat mengubah proteksi GCAST.")
        
    


    if len(args) < 2 or args[1].lower() not in ["on", "off"]:
        await message.reply("Gunakan: `/ankes on` atau `/ankes off`", quote=True)
        return

    state = args[1].lower() == "on"
    config[chat_id] = state
    save_config(config)
    x = await message.reply(f"<blockquote><b>Anti-GCAST telah {'AKTIF' if state else 'NONAKTIF'}.</b></blockquote>", quote=True)
    await asyncio.sleep(0.5)
    await x.delete()
        
    


# Assuming other imports and client initialization as before

async def is_admin(client, chat_id, user_id):
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


@app.on_message(filters.text & ~filters.private & Gcast)
async def delete_messages(client, message):
    try:
        chat_id = str(message.chat.id)
        if not config.get(chat_id, False):
            return

        # Admin tidak diproses
        if await is_admin(client, message.chat.id, message.from_user.id):
            return

        users = await get_white_ids(client.me.id)
        user_id = message.from_user.id

        # Jika user masuk whitelist, jangan hapus
        if user_id in users:
            return

        # Hapus pesan mencurigakan
        await message.delete()

        # Kirim peringatan
        user_mention = message.from_user.mention
        rs = "⚠️PERINGATAN"
        warn = await message.reply(
            f"<blockquote><i>{rs} {user_mention}, pesan lu jelek gua apus</i></blockquote>"
        )
        await asyncio.sleep(5)
        await warn.delete()

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except MessageDeleteForbidden:
        pass



