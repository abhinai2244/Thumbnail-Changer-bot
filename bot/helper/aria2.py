import asyncio
import os
import re
from bot.helper.task_manager import task_manager

class Aria2Downloader:
    async def download(self, url, path, task_id, filename=None):
        # aria2c -d "path" -o "filename" "url"
        cmd = [
            "aria2c",
            "--dir", path,
            "--max-connection-per-server=10",
            "--split=10",
            "--summary-interval=1", # Output summary every 1s
            url
        ]
        
        if filename:
             cmd.extend(["--out", filename])
             
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Monitor stdout for progress
        # Aria2 output format: [#2089b0 400.0KiB/33.5MiB(1%) CN:1 DL:115.7KiB ETA:4m51s]
        
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            
            line_str = line.decode().strip()
            if not line_str:
                continue
                
            # Regex to find (X%)
            match = re.search(r'\((\d+)%\)', line_str)
            if match:
                try:
                    percent = float(match.group(1))
                    await task_manager.update_progress(task_id, percent, "Downloading...")
                except:
                    pass
                    
        await process.wait()
        
        # Verify download
        if filename:
            full_path = os.path.join(path, filename)
            if os.path.exists(full_path):
                return full_path
        else:
            files = os.listdir(path)
            if files:
                files = [os.path.join(path, f) for f in files]
                files.sort(key=os.path.getsize, reverse=True)
                return files[0]
                
        return None

aria2 = Aria2Downloader()
