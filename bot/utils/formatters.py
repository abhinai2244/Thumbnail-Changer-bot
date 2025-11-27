import math

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)} {["B", "KB", "MB", "GB", "TB", "PB"][index]}'
    except IndexError:
        return 'File too large'

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def progress_bar(percentage):
    # Block quotes and emojis style
    completed = int(percentage / 10)
    return "🟩" * completed + "⬜" * (10 - completed)

async def progress_for_pyrogram(current, total, ud_type, message, start):
    import time
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = get_readable_time(elapsed_time / 1000)
        estimated_total_time = get_readable_time(estimated_total_time / 1000)

        progress = "<blockquote>"
        progress += f"**{ud_type}**\n"
        progress += f"{progress_bar(percentage)}\n"
        progress += f"**Progress:** {percentage:.2f}%\n"
        progress += f"**Done:** {get_readable_file_size(current)} of {get_readable_file_size(total)}\n"
        progress += f"**Speed:** {get_readable_file_size(speed)}/s\n"
        progress += f"**ETA:** {estimated_total_time}\n"
        progress += "</blockquote>"

        try:
            await message.edit(progress)
        except:
            pass
