import os
import zipfile
import shutil
import asyncio

async def zip_path(input_path, output_path=None):
    if not output_path:
        output_path = f"{input_path}.zip"
    
    parent_dir = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    
    # Run zip command from the parent directory to avoid full paths
    if os.path.isdir(input_path):
        cmd = ["zip", "-r", output_path, base_name]
    else:
        cmd = ["zip", output_path, base_name]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=parent_dir, # Set current working directory
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()
    
    if os.path.exists(output_path):
        return output_path
    return None

async def extract_path(input_path, output_dir=None):
    if not output_dir:
        output_dir = os.path.splitext(input_path)[0]
        os.makedirs(output_dir, exist_ok=True)
        
    cmd = ["unzip", input_path, "-d", output_dir]
    
    if input_path.endswith(".tar") or input_path.endswith(".tar.gz"):
        cmd = ["tar", "-xvf", input_path, "-C", output_dir]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()
    
    return output_dir
