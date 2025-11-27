import os
import subprocess
import asyncio
from bot.helper.task_manager import task_manager

async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = f"{output_directory}/{ttl}.jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None

async def set_thumbnail(video_file, thumbnail_file, output_path):
    # ffmpeg -i video.mp4 -i thumb.jpg -map 0 -map 1 -c copy -disposition:v:1 attached_pic output.mp4
    cmd = [
        "ffmpeg",
        "-i", video_file,
        "-i", thumbnail_file,
        "-map", "0",
        "-map", "1",
        "-c", "copy",
        "-disposition:v:1", "attached_pic",
        output_path
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.communicate()
    return output_path

async def rename_file(filepath, blacklist_words):
    dirname, filename = os.path.split(filepath)
    name, ext = os.path.splitext(filename)
    
    for word in blacklist_words:
        name = name.replace(word, "")
    
    name = name.strip()
    new_filename = f"{name}{ext}"
    new_filepath = os.path.join(dirname, new_filename)
    
    os.rename(filepath, new_filepath)
    return new_filepath
