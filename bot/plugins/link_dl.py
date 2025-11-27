from pyrogram import Client, filters
import os
import uuid
import shutil
import asyncio
import time
from bot.helper.task_manager import task_manager
from bot.helper.aria2 import aria2
from bot.helper.archiver import zip_path, extract_path
from bot.utils.formatters import progress_for_pyrogram
from bot.utils.cleanup import cleanup_task

@Client.on_message(filters.command("l"))
async def link_download_handler(client, message):
    user_id = message.from_user.id
    
    raw_args = ""
    if len(message.command) > 1:
        raw_args = message.text.split(" ", 1)[1]
    elif message.reply_to_message:
        # Check if reply has text
        content = message.reply_to_message.text or message.reply_to_message.caption
        if content:
            # Append arguments from current message if any (e.g. /l -z replying to link)
            current_args = message.text.split(" ", 1)[1] if len(message.command) > 1 else ""
            raw_args = f"{content} {current_args}"
    
    if not raw_args:
        await message.reply_text("Usage: `/l <url> [options]` or reply to a link.")
        return

    args_list = raw_args.split()
    
    url = None
    new_name = None
    do_zip = False
    do_extract = False
    
    # Heuristic parsing: URL is likely the first non-flag argument, but let's be careful.
    # We iterate and consume flags.
    
    skip_next = False
    for i, arg in enumerate(args_list):
        if skip_next:
            skip_next = False
            continue
            
        if arg == "-n":
            if i + 1 < len(args_list):
                new_name = os.path.basename(args_list[i+1])
                skip_next = True
        elif arg == "-z":
            do_zip = True
        elif arg == "-e":
            do_extract = True
        elif arg.startswith("http"):
            url = arg
            
    if not url:
        await message.reply_text("❌ No URL found.")
        return

    # Check Limits
    if not await task_manager.can_add_task(user_id):
        await message.reply_text("⚠️ System busy or you reached the limit.")
        return

    task_id = str(uuid.uuid4())[:8]
    await task_manager.add_task(user_id, task_id, "Direct Download")
    
    status_msg = await message.reply_text("<blockquote>Starting Direct Download...</blockquote>")
    
    try:
        temp_dir = f"downloads/{task_id}"
        os.makedirs(temp_dir, exist_ok=True)
        
        # 1. Download
        filepath = await aria2.download(url, temp_dir, task_id, filename=new_name)
        
        if not filepath:
            await status_msg.edit("❌ Download Failed.")
            return

        # 2. Post-Processing
        await status_msg.edit("<blockquote>Processing...</blockquote>")
        
        final_files = [filepath]
        
        if do_extract:
            extract_dir = await extract_path(filepath)
            # Remove the archive
            os.remove(filepath)
            # Collect extracted files
            final_files = []
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    final_files.append(os.path.join(root, file))
                    
        elif do_zip:
            zip_file = await zip_path(filepath)
            os.remove(filepath)
            final_files = [zip_file]

        # 3. Upload
        await status_msg.edit(f"<blockquote>Uploading {len(final_files)} file(s)...</blockquote>")
        
        for file in final_files:
            if os.path.getsize(file) == 0:
                continue
                
            await client.send_document(
                chat_id=message.chat.id,
                document=file,
                caption=f"**File:** `{os.path.basename(file)}`",
                progress=progress_for_pyrogram,
                progress_args=("Uploading", status_msg, time.time())
            )
            
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit(f"Error: {e}")
    finally:
        await task_manager.remove_task(task_id)
        await cleanup_task(f"downloads/{task_id}")
