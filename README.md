# 📈 Tuschology IDX Bot
Tuschology IDX Bot is an automated Discord & Telegram Bot that monitors:
- 🇮🇩 IDX (Indonesia Stock Exchange) official announcements
- 📰 Curated Indonesian financial RSS Feeds
- ⚠️ Priority alerts (Suspension, UMA, Disclosure, etc.)
It delivers structured, real-time notifications with dynamic Discord Rich Presence based on market conditions.

## ✨ Features
### 1. ⚠️ IDX Priority Monitoring (Level 2 Scraping)
- Scrapes official IDX announcement page.
- Detects:
  - Supension (Suspensi)
  - Unusual Market Activity (UMA)
  - Disclosure / Keterbukaan Informasi
  - General issuer announcements
   
- Extracts:
  - Announcement category
  - Title
  - Direct link
- Prevents duplicate alerts vie persistent hash tracking
- Maintenance detection & auto status switching

### 2. 📰 Financial Media RSS Monitoring
- Monitors selected financial sources:
  - CNBC Indonesia
  - CNN Indonesia
  - Tempo Bisnis
  - Antara
  - Kontan
  - Bloomberg Technoz

- Features:
  - Keyword filtering
  - Duplicate prevention
  - Age filtering (max 3 days)
  - Multi-source aggregation

### 3. 💬 Discord Integration
- Topic-based routing (send only to channels with marker ***```TCHNEWS```***)
- Multi-server compatible
- Dynamic Rich Presence:
  - IDX Maintenance
  - IDX Priority Alert
  - Market Closed
  - IDX & Market News
- Automatic presence switching based on market hours

### 4. 💬 Telegram Integration
- Broadcast alerts to Telegram channel/group
- ***```/status```*** command via DM only
- Real-time system status:
  - Feeds count
  - Last RSS check (seconds)
  - Last news time
  - IDX status (ACTIVE / MAINTENANCE / OFFLINE)
  
  Example:
    ```
    🟢 IDX News Bot — ONLINE
    📡 Feeds aktif: 6
    ⏱ Last RSS check: 8 detik lalu
    📰 Last news: N/A lalu
    📊 IDX Status: ACTIVE
    ```
### 5. 🔁 Stability & Reliability
- Persistent JSON state storage
- Duplicate detection cache
- Maintenance detection logic
- Async pipelines
- systemd-ready deployment

## 📁 Project Structure
```
idx_bot/
│
├── main.py
├── config.py
├── .env
│
├── core/
│   ├── state.py
│   ├── filters.py
│   ├── market.py
│   ├── utils.py
│   └── fetchers.py
│
├── pipelines/
│   ├── idx.py
│   └── media.py
│
└── platforms/
    ├── discord.py
    └── telegram.py
```

## ⚙️ Installation Guide
### 1. Clone Repository
```
git clone https://github.com/demuuus/Tuschology-IDX-Bot.git
cd Tuschology-IDX-Bot/idx_bot
```

### 2. Create Virtual Environment
Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```
Windows:
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
Create ***```requirements.txt```***:
```
discord.py
python-telegram-bot
beautifulsoup4
aiohttp
feedparser
python-dotenv
```
Install:
```
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create ***```.env```*** file:
```
DISCORD_TOKEN=your_discord_bot_token
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```
Make sure ***```.env```*** is in ***```.gitignore```***.

### 5. Configure Discord Channel Routing
Add this text inside your Discord channel topic:
```
TCHNEWS
```
Bot will automatically send messages only to channels containing this marker.

### 6. Run the Bot
```
python3 main.py
```
If successful:
```
✅ Tuschology is online
```

## 🚀 Production Deployment**
Use **systemd** on VPS.
Create:
```
/etc/systemd/system/tuschology.service
```
Example:
```
[Unit]
Description=Tuschology IDX Bot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/idx_bot
ExecStart=/home/ubuntu/idx_bot/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Then:
```
sudo systemctl daemon-reload
sudo systemctl enable tuschology
sudo systemctl start tuschology
```

## 📊 Market Hours Logic
Bot automatically detects:
  - Weekends -> Market Closed
  - 09:00 - 12:00 WIB -> Open
  - 12:00 - 13:00 WIB -> Break
  - 13:00 - 16:00 WIB -> Open
  - After 16:00 -> Closed
Presence updates accordingly
