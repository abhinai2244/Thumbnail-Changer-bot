from pyrogram import Client, filters
from bot.helper.task_manager import task_manager
import time

@Client.on_message(filters.command("status"))
async def status_command(client, message):
    tasks = task_manager.get_all_tasks()
    if not tasks:
        await message.reply_text("No active tasks.")
        return

    msg = "<blockquote>**Active Tasks**</blockquote>\n\n"
    for task_id, info in tasks.items():
        msg += f"**Task ID:** `{task_id}`\n"
        msg += f"**Type:** {info['type']}\n"
        msg += f"**Status:** {info['status']}\n"
        msg += f"**Progress:** {info['progress']}%\n"
        msg += "------------------------\n"
    
    await message.reply_text(msg)
