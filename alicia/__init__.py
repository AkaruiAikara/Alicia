import sys
import logging

import spamwatch
from pyrogram import Client
from configparser import ConfigParser

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

LOGGER.info("Starting Alicia...")

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

parser = ConfigParser()
parser.read("config.ini")
botconfig = parser["botconfig"]

OWNER_ID = botconfig.getint("OWNER_ID")
DB_URI = botconfig.get("DB_URI")
LOAD = botconfig.get("LOAD").split()
LOAD = list(map(str, LOAD))
NOLOAD = botconfig.get("NOLOAD").split()
NOLOAD = list(map(str, NOLOAD))
MESSAGE_DUMP = botconfig.get("MESSAGE_DUMP")
IMG = botconfig.get("IMG")
ARL = botconfig.get("ARL")
LASTFM_API_KEY = botconfig.get("LASTFM_API_KEY")
API_WEATHER = botconfig.get("API_WEATHER")
SPAMWATCH = botconfig.get("SPAMWATCH")
WALL_API = botconfig.get("WALL_API")
BRAINLY_API = botconfig.get("BRAINLY_API")


alia = Client(":memory:", config_file="config.ini")

bot_name = ""
bot_username = ""
bot_id = 0

if SPAMWATCH is None:
    spamwtc = None
    LOGGER.warning("Invalid spamwatch api")
else:
    spamwtc = spamwatch.Client(SPAMWATCH)

async def get_bot():
    global bot_id, bot_name, bot_username
    getbot = await alia.get_me()
    bot_id = getbot.id
    bot_name = getbot.first_name
    bot_username = getbot.username 
