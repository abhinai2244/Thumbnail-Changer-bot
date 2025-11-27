from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from bot.helper.database import db
import os

@Client.on_message(filters.command("settings"))
async def settings(client, message):
    user_id = message.from_user.id
    
    # Inline keyboard for settings
    buttons = [
        [InlineKeyboardButton("🖼️ Set Thumbnail", callback_data="set_thumb")],
        [InlineKeyboardButton("🚫 Set Blacklist", callback_data="set_blacklist")],
        [InlineKeyboardButton("🗑️ Clear Thumbnail", callback_data="clear_thumb")],
        [InlineKeyboardButton("👀 View Settings", callback_data="view_settings")]
    ]
    
    await message.reply_text(
        "<blockquote>**Settings Menu**</blockquote>\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    
    if data == "set_thumb":
        await query.message.edit_text("Send me a photo to set as your thumbnail.")
        # In a real scenario, we'd use a state machine (conversation handler)
        # For simplicity, we can ask the user to reply to this message or just send a photo next.
        # Here we will register a next_step_handler logic or simple instructions.
        # Since Pyrofork doesn't have built-in conversation handler like Telethon, we can use a global dict or listen to next photo.
        # But to keep it simple and robust, let's just instruct:
        await query.message.reply_text("Please send the photo you want to set as thumbnail and reply to it with `/set_thumb` command.")

    elif data == "set_blacklist":
        await query.message.edit_text("Send me words to remove from filenames separated by comma.\nExample: `/set_blacklist www.site.com, @channelname`")
        
    elif data == "clear_thumb":
        await db.set_thumbnail(user_id, None)
        await query.answer("Thumbnail cleared!", show_alert=True)
        
    elif data == "view_settings":
        thumb = await db.get_thumbnail(user_id)
        blacklist = await db.get_blacklist(user_id)
        
        txt = "<blockquote>**Your Settings**</blockquote>\n\n"
        txt += f"**Thumbnail:** {'Set ✅' if thumb else 'Not Set ❌'}\n"
        txt += f"**Blacklist Words:** {', '.join(blacklist) if blacklist else 'None'}\n"
        
        await query.message.edit_text(txt)

@Client.on_message(filters.command("set_thumb") & filters.reply)
async def set_thumb_reply(client, message):
    if message.reply_to_message.photo:
        # Download photo to get file_id or keep file_id
        # We can just store file_id if we want to send it, but for ffmpeg we need to download it every time or store it locally.
        # Storing locally is better for ffmpeg.
        
        photo = message.reply_to_message.photo
        file_id = photo.file_id
        # We will store the file_id and download it when needed, or download now and store path.
        # Since we use docker, persistent storage might be an issue if we don't map volumes.
        # Let's store file_id in DB, and download on demand.
        
        await db.set_thumbnail(message.from_user.id, file_id)
        await message.reply_text("Thumbnail saved successfully!")
    else:
        await message.reply_text("Reply to a photo.")

@Client.on_message(filters.command("set_blacklist"))
async def set_blacklist_cmd(client, message):
    try:
        text = message.text.split(None, 1)[1]
        words = [w.strip() for w in text.split(",")]
        await db.set_blacklist(message.from_user.id, words)
        await message.reply_text(f"Blacklist updated: {words}")
    except IndexError:
        await message.reply_text("Usage: `/set_blacklist word1, word2`")
