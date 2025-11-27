import yt_dlp
import asyncio
import os
import uuid
from bot.helper.task_manager import task_manager

class Downloader:
    def __init__(self):
        pass

    async def download(self, url, path, task_id, progress_callback=None):
        loop = asyncio.get_running_loop()
        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'progress_hooks': [lambda d: self._hook(d, task_id, progress_callback, loop)],
            'quiet': True,
            'noplaylist': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                await loop.run_in_executor(None, lambda: ydl.download([url]))
            
            # Find the downloaded file
            for file in os.listdir(path):
                return os.path.join(path, file)
        except Exception as e:
            print(f"Download Error: {e}")
            return None

    def _hook(self, d, task_id, progress_callback, loop):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%', '')
                progress = float(p)
                if progress_callback:
                    asyncio.run_coroutine_threadsafe(
                        task_manager.update_progress(task_id, progress, "Downloading..."),
                        loop
                    )
            except:
                pass

downloader = Downloader()
