# 🤖 Media Downloader Bot

A powerful Telegram bot built with **Pyrofork** and **MongoDB** to download media, manage files, and process tasks efficiently.

## ✨ Features

- **🚀 Smart Downloader:** Downloads videos from social sites (YouTube, Instagram, etc.) using `yt-dlp`.
- **⚡ Direct Links:** High-speed downloads for direct files using `aria2`.
- **📦 Archive Tools:** Built-in support to **Zip** or **Extract** downloaded files automatically.
- **🖼️ Custom Thumbnails:** Users can set a permanent custom thumbnail for all their video downloads.
- **🚫 Filename Cleaner:** Automatically remove specific words (like website ads) from filenames.
- **🛡️ Task Manager:** Robust queue system with concurrent task limits.
- **🐳 Dockerized:** Easy deployment with Docker and Docker Compose.
- **🎨 Modern UI:** Beautiful interface using Telegram's new Block Quotes and Emojis.

## 🛠️ Installation & Setup

### Prerequisites
- Docker & Docker Compose installed on your server.
- A Telegram Bot Token (@BotFather).
- Telegram API ID & Hash (my.telegram.org).
- MongoDB Connection String.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/media-bot.git
cd media-bot
```

### 2. Configure Environment
Rename the example config file and edit it:
```bash
mv config.env.sample config.env
nano config.env
```

**Variables:**
- `API_ID` & `API_HASH`: Get from my.telegram.org.
- `BOT_TOKEN`: Get from @BotFather.
- `MONGO_DB_URI`: Your MongoDB URL (e.g., `mongodb://mongo:27017` if using internal docker).
- `OWNER_ID`: Your Telegram User ID (for admin commands).
- `MAX_CONCURRENT_TASKS`: (Optional) Default limit for simultaneous downloads.

### 3. Run with Docker
Start the bot and database:
```bash
docker-compose up -d --build
```

The bot should now be online! 🟢

## 🎮 Commands

### Media Commands
- `/dl <link>` - Download video/audio from supported sites (YouTube, Instagram, etc.).
  - *Applies your custom thumbnail and filename blacklist settings automatically.*

### Direct Link Commands
- `/l <link> [options]` - Download files from a direct URL.
  
  **Options:**
  - `-n <name>` : Rename the file (e.g., `/l http://file.mp4 -n myvideo.mp4`).
  - `-z` : Zip the downloaded file/folder.
  - `-e` : Extract the downloaded archive (zip/tar/tar.gz).
  
  **Examples:**
  > `/l http://example.com/archive.zip -e` (Download & Extract)
  > `/l http://example.com/video.mp4 -n cool_video.mp4` (Download & Rename)

### General Commands
- `/start` - Check if the bot is alive.
- `/status` - Check current active tasks and progress.
- `/settings` - Open the settings menu to:
  - 🖼️ Set/Clear Custom Thumbnail.
  - 🚫 Manage Filename Blacklist.

### Owner Commands
- `/owner limit <number>` - Set the global maximum concurrent tasks (e.g., `/owner limit 10`).

## 📂 Directory Structure
- `bot/plugins`: Command handlers (separated by functionality).
- `bot/helper`: Core logic (Database, Downloader, Aria2, Archiver).
- `downloads/`: Temporary folder for active downloads.

## 📝 Credits
- Built using [Pyrofork](https://github.com/Mayuri-Chan/Pyrofork).
- Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) & [aria2](https://github.com/aria2/aria2).
