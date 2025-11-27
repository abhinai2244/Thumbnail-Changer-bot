from pyrogram import Client, filters
from bot.helper.database import db

@Client.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
    
    txt = (
        "<blockquote>**Welcome to the Media Bot!**</blockquote>\n\n"
        "I can help you download media, manage files, and more.\n"
        "Use /settings to configure your preferences.\n"
        "Use /dl <link> to download media."
    )
    await message.reply_text(txt)
