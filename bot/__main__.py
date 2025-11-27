from pyrogram import Client
from pyrogram.enums import ParseMode
from bot.config import Config
import os

# Create download directory
if not os.path.exists("downloads"):
    os.makedirs("downloads")

plugins = dict(root="bot/plugins")

app = Client(
    "media_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=plugins,
    parse_mode=ParseMode.HTML
)

if __name__ == "__main__":
    print("Bot Starting...")
    app.run()
