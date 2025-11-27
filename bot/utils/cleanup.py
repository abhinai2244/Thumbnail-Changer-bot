import shutil
import asyncio
import os

async def cleanup_task(path):
    if not os.path.exists(path):
        return

    for i in range(5):
        try:
            shutil.rmtree(path, ignore_errors=False)
            break
        except OSError:
            await asyncio.sleep(1 + i) # Wait 1s, 2s, 3s...
            
    # Final attempt with ignore_errors
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
