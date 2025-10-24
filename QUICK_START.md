# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

Open Command Prompt or PowerShell and run:

```bash
pip install -r requirements.txt
```

### Step 2: Setup IP Webcam (1 minute)

1. Install **IP Webcam** app on your Android phone (Google Play Store)
2. Open the app
3. Scroll down and tap **"Start Server"**
4. Note the IP address shown (e.g., `http://10.10.70.17:8080`)

### Step 3: Create Telegram Bot (2 minutes)

#### Get Bot Token:
1. Open Telegram, search for `@BotFather`
2. Send: `/newbot`
3. Follow the prompts to name your bot
4. **Copy the token** (looks like: `123456789:ABCdefGhI...`)

#### Get Chat ID:
1. Start a chat with your new bot
2. Send it any message (e.g., "Hello")
3. Open in browser (replace `YOUR_BOT_TOKEN`):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
4. Find and copy your chat ID (the number after `"chat":{"id":`)

### Step 4: Configure (30 seconds)

**Option A - Use GUI (Recommended)**

1. Double-click `start_launcher.bat` or run `python launcher.py`
2. Fill in the form:
   - IP Address: `10.10.70.17` (from IP Webcam)
   - Port: `8080`
   - Bot Token: (paste your token)
   - Chat ID: (paste your chat ID)
3. Click **"Save Configuration"**

**Option B - Edit Manually**

Edit `config.json`:
```json
{
    "ip_webcam": {
        "ip_address": "10.10.70.17",  // Your IP
        "port": "8080"
    },
    "telegram": {
        "bot_token": "123456789:ABC...",  // Your token
        "chat_id": "987654321"             // Your chat ID
    }
}
```

### Step 5: Test & Run (30 seconds)

1. Click **"Test Telegram"** to verify connection ✅
2. Click **"▶ Start Detection"** to begin monitoring
3. Try lying down on the floor to test fall detection!

---

## 📱 Troubleshooting

**Can't connect to IP Webcam?**
- Make sure phone and computer are on same WiFi
- Check IP address is correct
- Try opening `http://10.10.70.17:8080/video` in a browser

**Telegram not working?**
- Verify you sent a message to your bot first
- Check token and chat ID have no extra spaces
- Use "Test Telegram" button

**Fall detection not working?**
- Ensure good lighting
- Make sure full body is visible
- Try adjusting confidence threshold (lower = more sensitive)

---

## 🎯 Quick Tips

- **Press 'q'** in the detection window to stop
- **Press 't'** to send a test alert
- Check `fall_screenshots/` folder for saved images
- View `fall_detection.log` for activity history

---

## 🎮 Two Ways to Run

### Method 1: GUI Launcher (Easier)
```bash
python launcher.py
```
or double-click `start_launcher.bat`

### Method 2: Direct Script
```bash
python fall_detection.py
```

---

**Need more help?** Check `README.md` for detailed documentation.
