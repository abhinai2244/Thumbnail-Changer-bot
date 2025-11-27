from pyrogram import Client, filters
from bot.helper.database import db
from bot.config import Config

@Client.on_message(filters.command("owner") & filters.user(Config.OWNER_ID))
async def owner_settings(client, message):
    try:
        # Simple command to set concurrency
        # Usage: /owner limit 10
        cmd = message.text.split()
        if len(cmd) > 2 and cmd[1] == "limit":
            limit = int(cmd[2])
            await db.set_concurrency_limit(limit)
            await message.reply_text(f"✅ Global concurrency limit set to **{limit}**.")
        else:
            current = await db.get_concurrency_limit()
            await message.reply_text(
                f"<blockquote>**Owner Settings**</blockquote>\n"
                f"**Current Concurrency Limit:** {current}\n\n"
                "**Usage:**\n`/owner limit <number>`"
            )
    except Exception as e:
        await message.reply_text(f"Error: {e}")
