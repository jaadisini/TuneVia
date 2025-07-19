import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters


load_dotenv()

# ───── Basic Bot Configuration ───── #
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_ID = int(getenv("OWNER_ID", 6305402536))
OWNER_USERNAME = getenv("OWNER_USERNAME", "Dzkyou")
BOT_USERNAME = getenv("BOT_USERNAME", "aleamusicbot")
BOT_NAME = getenv("BOT_NAME", "ᴀʟᴇ ᴍᴜsɪᴄ")
ASSUSERNAME = getenv("ASSUSERNAME", "Imtakyoo")
EVALOP = list(map(int, getenv("EVALOP", "6305402536").split()))

# ───── Mongo & Logging ───── #
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOGGER_ID = int(getenv("LOGGER_ID", "-1002730786733"))

# ───── Limits and Durations ───── #
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

# ───── Custom API Configs ───── #
COOKIE_URL = getenv("COOKIE_URL"  "https://pastebin.com/twh5xXun") #necessary
API_URL = getenv("API_URL") #optional
API_KEY = getenv("API_KEY") #optional

# ───── Heroku Configuration ───── #
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ───── Git & Updates ───── #
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/jaadisini/TuneVia")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN")

# ───── Support & Community ───── #
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/dzdisni")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/DZareaa")

# ───── Assistant Auto Leave ───── #
AUTO_LEAVING_ASSISTANT = False
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "11500"))

# ───── Error Handling ───── #
DEBUG_IGNORE_LOG =True

# ───── Spotify Credentials ───── #
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773")

# ───── Session Strings ───── #
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")

# ───── Server Settings ───── #
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "3000"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "2500"))

# ───── Bot Media Assets ───── #
START_VIDS = [
    "https://files.catbox.moe/a2d9ok.jpg",
]

STICKERS = [
    "CAACAgUAAx0Cd6nKUAACASBl_rnalOle6g7qS-ry-aZ1ZpVEnwACgg8AAizLEFfI5wfykoCR4h4E",
    "CAACAgUAAx0Cd6nKUAACATJl_rsEJOsaaPSYGhU7bo7iEwL8AAPMDgACu2PYV8Vb8aT4_HUPHgQ"
]
HELP_IMG_URL = "https://files.catbox.moe/1zpysu.jpg"
PING_VID_URL = "https://files.catbox.moe/1zpysu.jpg"
PLAYLIST_IMG_URL = "https://files.catbox.moe/1zpysu.jpg"
STATS_VID_URL = "https://files.catbox.moe/1zpysu.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/1zpysu.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/1zpysu.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/1zpysu.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/1zpysu.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/1zpysu.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/1zpysu.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/1zpysu.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/1zpysu.jpg"
FAILED = "https://files.catbox.moe/a2d9ok.jpg"

# ───── Utility & Functional ───── #
def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")


# ───── Bot Introduction Messages ───── #
AYU = ["🔍", "⚡️", "🔥"]


# ───── Runtime Structures ───── #
BANNED_USERS = filters.user()
adminlist, lyrical, votemode, autoclean, confirmer = {}, {}, {}, [], {}

# ───── URL Validation ───── #
if SUPPORT_CHANNEL and not re.match(r"^https?://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHANNEL URL. Must start with https://")

if SUPPORT_CHAT and not re.match(r"^https?://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHAT URL. Must start with https://")
