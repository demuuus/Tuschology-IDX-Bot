# **📈 Tuschology IDX Bot**
Tuschology IDX Bot is an automated Discord & Telegram Bot that monitors:
- 🇮🇩 IDX (Indonesia Stock Exchange) official announcements
- 📰 Curated Indonesian financial RSS Feeds
- ⚠️ Priority alerts (Suspension, UMA, Disclosure, etc.)
It delivers structured, real-time notifications with dynamic Discord Rich Presence based on market conditions.

## **✨ Features**
### **1. ⚠️ IDX Priority Monitoring (Level 2 Scraping)**
* Scrapes official IDX announcement page.
* Detects:
 - Supension (Suspensi)
 - Unusual Market Activity (UMA)
 - Disclosure / Keterbukaan Informasi
 - General issuer announcements
   
  • Extracts:
     - Announcement category
     - Title
     - Direct link
  • Prevents duplicate alerts vie persistent hash tracking
  • Maintenance detection & auto status switching

### **2. 📰 Financial Media RSS Monitoring**
   Monitors selected financial sources:
     • CNBC Indonesia
     • CNN Indonesia
     • Tempo Bisnis
     • Antara
     • Kontan
     • Bloomberg Technoz

   Features:
     • Keyword filtering
     • Duplicate prevention
     • Age filtering (max 3 days)
     • Multi-source aggregation

### **3. 💬 Discord Integration**
  • Topic-based routing (send only to channels with marker ***TCHNEWS***)
  • Multi-server compatible
  • Dynamic Rich Presence:
    - IDX Maintenance
    - IDX Priority Alert
    - Market Closed
    - IDX & Market News
  • Automatic presence switching based on market hours

### **4. 💬 Telegram Integration**
  • Broadcast alerts to Telegram channel/group
  • ***/status*** command via DM only
  • Real-time system status:
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
    
