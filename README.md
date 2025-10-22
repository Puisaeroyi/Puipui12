# Human Fall Detection System

A real-time fall detection system using MediaPipe Pose Estimation and IP Webcam that sends instant alerts to Telegram.

## Features

- **Real-time Pose Estimation**: Uses MediaPipe for accurate human pose detection
- **Fall Detection**: Intelligent algorithm to detect when a person has fallen
- **Telegram Alerts**: Instant notifications with timestamp and screenshot
- **Cooldown Mechanism**: Prevents alert spam with configurable cooldown period
- **Logging System**: Complete activity logs for review
- **Manual Testing**: Built-in test function to verify Telegram connectivity
- **CPU Optimized**: Runs efficiently on CPU without requiring GPU

## Requirements

- Windows OS (tested on Windows)
- Python 3.8 or higher
- IP Webcam app on your phone (available on Google Play Store)
- Telegram Bot (instructions below)
- Phone and computer on the same local network

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup IP Webcam on Your Phone

1. Download and install **IP Webcam** from Google Play Store
2. Open the app and scroll to the bottom
3. Tap "Start Server"
4. Note the IP address shown (e.g., http://10.10.70.17:8080)
5. Make sure your phone and computer are on the same WiFi network

### 3. Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the **Bot Token** (looks like: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`)
5. Start a chat with your new bot and send any message

### 4. Get Your Telegram Chat ID

1. Open this URL in your browser (replace YOUR_BOT_TOKEN):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
2. Look for `"chat":{"id":123456789}` in the response
3. Copy the number after `"id":` (this is your Chat ID)

### 5. Configure the System

Edit `config.json` and update:

```json
{
    "ip_webcam": {
        "ip_address": "10.10.70.17",  // Your IP Webcam address
        "port": "8080",
        "stream_path": "/video"
    },
    "telegram": {
        "bot_token": "YOUR_BOT_TOKEN_HERE",  // Paste your bot token
        "chat_id": "YOUR_CHAT_ID_HERE"       // Paste your chat ID
    },
    ...
}
```

## Usage

### Running the System

Simply run the main script:

```bash
python fall_detection.py
```

### Controls

- **Press 'q'**: Quit the program
- **Press 't'**: Send a test alert to Telegram

### What Happens When a Fall is Detected

1. System detects a person in a fallen position
2. Calculates confidence level
3. If confidence > threshold (default 70%), sends alert
4. Telegram receives:
   - Alert message with timestamp
   - Screenshot of the detected fall
   - Confidence level and body angle
5. Cooldown period activated (default 30 seconds)

## Configuration Options

Edit `config.json` to customize:

### Detection Settings

- **confidence_threshold**: Minimum confidence (0.0-1.0) required to trigger alert (default: 0.7)
- **fall_angle_threshold**: Body angle threshold in degrees (default: 60)
- **cooldown_seconds**: Time between alerts (default: 30)
- **min_detection_confidence**: MediaPipe detection confidence (default: 0.5)

### System Settings

- **fps**: Frames processed per second (default: 10)
- **screenshot_quality**: JPEG quality 1-100 (default: 90)
- **log_file**: Path to log file
- **screenshots_folder**: Folder for saved screenshots

## How Fall Detection Works

The system uses a multi-factor approach:

1. **Body Angle Analysis**: Detects if the body is horizontal (< 60° from horizontal)
2. **Vertical Position**: Checks if the person is in the lower part of the frame
3. **Height Difference**: Measures if shoulders and hips are at similar height (flat position)

All three factors are combined with weighted confidence scoring.

## Troubleshooting

### Cannot Connect to IP Webcam

- Ensure IP Webcam is running and server is started
- Verify IP address in config.json matches the one shown in IP Webcam
- Make sure both devices are on the same WiFi network
- Try accessing the stream in a browser: `http://10.10.70.17:8080/video`

### Telegram Alerts Not Sending

- Verify bot token is correct (no extra spaces)
- Verify chat ID is correct (should be a number)
- Make sure you've sent at least one message to your bot
- Test using the 't' key while the program is running
- Check the log file for error messages

### Poor Detection Accuracy

- Ensure good lighting conditions
- Make sure the person is fully visible in frame
- Adjust `confidence_threshold` in config.json (lower = more sensitive)
- Adjust `fall_angle_threshold` for different detection sensitivity
- Check that camera is relatively stable (not moving)

### High CPU Usage

- Reduce `fps` in config.json (default: 10)
- Lower camera resolution in IP Webcam settings
- Close other CPU-intensive applications

## File Structure

```
fall-detection-system/
│
├── fall_detection.py       # Main detection script
├── config.json             # Configuration file
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── fall_detection.log     # Log file (created on first run)
│
└── fall_screenshots/      # Screenshot folder (created on first run)
    └── fall_YYYYMMDD_HHMMSS.jpg
```

## Log Files

All events are logged to `fall_detection.log`:
- System start/stop
- Connection status
- Fall detections
- Alerts sent
- Errors and warnings

Review this file to see the complete history of the system's operation.

## Testing

1. **Test Telegram Connection**: Press 't' while the system is running
2. **Test Fall Detection**: Stand in front of camera, then lie down on the floor
3. **Verify Screenshot**: Check `fall_screenshots/` folder after an alert

## Tips for Best Results

1. **Camera Placement**: Position camera to capture full body of the person
2. **Lighting**: Ensure adequate lighting for better pose detection
3. **Background**: Clearer backgrounds improve detection accuracy
4. **Camera Stability**: Keep camera/phone stable (use a stand or mount)
5. **Network**: Use strong WiFi connection for reliable streaming
6. **Testing**: Run several tests to find optimal threshold values for your setup

## Privacy & Security

- All processing is done locally on your computer
- No data is sent to external servers except Telegram alerts
- Screenshots are stored locally only
- The system only monitors when actively running

## License

This project is for educational and personal use.

## Support

For issues or questions, review the log file first, then check the troubleshooting section above.

---

**Created for testing and educational purposes. Use responsibly.**
