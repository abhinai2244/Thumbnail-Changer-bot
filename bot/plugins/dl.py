from pyrogram import Client, filters
import os
import uuid
import shutil
from bot.helper.task_manager import task_manager
from bot.helper.downloader import downloader
from bot.helper.database import db
from bot.helper.ffmpeg import set_thumbnail, rename_file
from bot.utils.formatters import progress_for_pyrogram
from bot.utils.cleanup import cleanup_task
import time
import asyncio

@Client.on_message(filters.command("dl"))
async def download_handler(client, message):
    user_id = message.from_user.id
    
    url = None
    if len(message.command) > 1:
        url = message.command[1]
    elif message.reply_to_message:
        url = message.reply_to_message.text or message.reply_to_message.caption
    
    if not url:
        await message.reply_text("Usage: `/dl <url>` or reply to a link.")
        return
    
    # Simple URL cleanup (in case of extra text)
    if "http" in url:
        # Extract first url found
        import re
        urls = re.findall(r'(https?://\S+)', url)
        if urls:
            url = urls[0]
        else:
            await message.reply_text("❌ No valid URL found.")
            return
    else:
        await message.reply_text("❌ No valid URL found.")
        return
    
    # 1. Check Limits
    if not await task_manager.can_add_task(user_id):
        await message.reply_text("⚠️ System busy or you reached the limit. Try again later.")
        return

    task_id = str(uuid.uuid4())[:8]
    await task_manager.add_task(user_id, task_id, "Download")
    
    status_msg = await message.reply_text("<blockquote>Initializing download...</blockquote>")
    
    try:
        # Create temp dir
        temp_dir = f"downloads/{task_id}"
        os.makedirs(temp_dir, exist_ok=True)
        
        # 2. Download
        start_time = time.time()
        filepath = await downloader.download(
            url, 
            temp_dir, 
            task_id, 
            progress_callback=True
        )
        
        if not filepath:
            await status_msg.edit("❌ Download Failed.")
            await task_manager.remove_task(task_id)
            return

        # 3. Process (Thumbnail & Rename)
        await status_msg.edit("<blockquote>Processing File...</blockquote>")
        await task_manager.update_progress(task_id, 100, "Processing")

        # Rename (Blacklist)
        blacklist = await db.get_blacklist(user_id)
        if blacklist:
            filepath = await rename_file(filepath, blacklist)

        # Thumbnail
        thumb_id = await db.get_thumbnail(user_id)
        thumb_path = None
        if thumb_id:
            try:
                # Download user thumbnail
                thumb_path = await client.download_media(thumb_id, file_name=f"{temp_dir}/thumb.jpg")
                # Apply thumbnail using ffmpeg
                # This creates a NEW file with attached pic
                out_path = f"{temp_dir}/out_{os.path.basename(filepath)}"
                await set_thumbnail(filepath, thumb_path, out_path)
                # cleanup old file
                os.remove(filepath)
                filepath = out_path
            except Exception as e:
                print(f"Thumbnail Error: {e}")
                # If fail, proceed with original file
                pass
        
        # 4. Upload
        await status_msg.edit("<blockquote>Uploading...</blockquote>")
        await task_manager.update_progress(task_id, 0, "Uploading")
        
        await client.send_document(
            chat_id=message.chat.id,
            document=filepath,
            thumb=thumb_path if thumb_path else None, # Use the downloaded jpg as telegram thumb too
            caption=f"**File:** `{os.path.basename(filepath)}`",
            progress=progress_for_pyrogram,
            progress_args=("Uploading", status_msg, time.time())
        )
        
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit(f"Error: {e}")
    finally:
        await task_manager.remove_task(task_id)
        # Cleanup
        await cleanup_task(f"downloads/{task_id}")
