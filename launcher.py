"""
Fall Detection System - Simple GUI Launcher
Provides an easy way to start and manage the fall detection system
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import subprocess
import os
import sys
from pathlib import Path
import threading


class FallDetectionLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Fall Detection System - Launcher")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        self.config_file = "config.json"
        self.process = None

        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="Human Fall Detection System",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)

        # Main content
        content_frame = tk.Frame(self.root, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Configuration Section
        config_label = tk.Label(
            content_frame,
            text="Configuration",
            font=("Arial", 14, "bold")
        )
        config_label.pack(anchor=tk.W, pady=(0, 10))

        # IP Webcam settings
        ip_frame = tk.LabelFrame(content_frame, text="IP Webcam Settings", padx=10, pady=10)
        ip_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(ip_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ip_entry = tk.Entry(ip_frame, width=30)
        self.ip_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        tk.Label(ip_frame, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.port_entry = tk.Entry(ip_frame, width=30)
        self.port_entry.grid(row=1, column=1, pady=5, padx=(10, 0))

        # Telegram settings
        telegram_frame = tk.LabelFrame(content_frame, text="Telegram Settings", padx=10, pady=10)
        telegram_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(telegram_frame, text="Bot Token:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.token_entry = tk.Entry(telegram_frame, width=30, show="*")
        self.token_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        tk.Label(telegram_frame, text="Chat ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.chatid_entry = tk.Entry(telegram_frame, width=30)
        self.chatid_entry.grid(row=1, column=1, pady=5, padx=(10, 0))

        # Detection settings
        detection_frame = tk.LabelFrame(content_frame, text="Detection Settings", padx=10, pady=10)
        detection_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(detection_frame, text="Confidence Threshold:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.confidence_entry = tk.Entry(detection_frame, width=30)
        self.confidence_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        tk.Label(detection_frame, text="Cooldown (seconds):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cooldown_entry = tk.Entry(detection_frame, width=30)
        self.cooldown_entry.grid(row=1, column=1, pady=5, padx=(10, 0))

        # Save button
        save_btn = tk.Button(
            content_frame,
            text="Save Configuration",
            command=self.save_config,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            cursor="hand2"
        )
        save_btn.pack(pady=10)

        # Control buttons
        btn_frame = tk.Frame(content_frame)
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ Start Detection",
            command=self.start_detection,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            cursor="hand2"
        )
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(
            btn_frame,
            text="⬛ Stop Detection",
            command=self.stop_detection,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.stop_btn.grid(row=0, column=1, padx=5)

        # Additional buttons
        extra_btn_frame = tk.Frame(content_frame)
        extra_btn_frame.pack(pady=10)

        test_btn = tk.Button(
            extra_btn_frame,
            text="Test Telegram",
            command=self.test_telegram,
            bg="#f39c12",
            fg="white",
            font=("Arial", 10),
            width=15,
            cursor="hand2"
        )
        test_btn.grid(row=0, column=0, padx=5)

        log_btn = tk.Button(
            extra_btn_frame,
            text="View Logs",
            command=self.view_logs,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10),
            width=15,
            cursor="hand2"
        )
        log_btn.grid(row=0, column=1, padx=5)

        screenshots_btn = tk.Button(
            extra_btn_frame,
            text="Open Screenshots",
            command=self.open_screenshots,
            bg="#16a085",
            fg="white",
            font=("Arial", 10),
            width=15,
            cursor="hand2"
        )
        screenshots_btn.grid(row=0, column=2, padx=5)

        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            bg="#34495e",
            fg="white",
            font=("Arial", 10),
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def create_default_config(self):
        """Create default configuration file if it doesn't exist"""
        default_config = {
            "ip_webcam": {
                "ip_address": "10.10.70.17",
                "port": "8080",
                "stream_path": "/video"
            },
            "telegram": {
                "bot_token": "YOUR_BOT_TOKEN_HERE",
                "chat_id": "YOUR_CHAT_ID_HERE"
            },
            "detection": {
                "confidence_threshold": 0.7,
                "fall_angle_threshold": 60,
                "cooldown_seconds": 30,
                "min_detection_confidence": 0.5
            },
            "system": {
                "fps": 10,
                "screenshot_quality": 90,
                "log_file": "fall_detection.log",
                "screenshots_folder": "fall_screenshots"
            }
        }

        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=4)

        return default_config

    def load_config(self):
        """Load configuration from file"""
        try:
            # Check if config file exists, if not create it
            if not os.path.exists(self.config_file):
                messagebox.showinfo(
                    "First Time Setup",
                    "Config file not found. Creating default configuration.\n\n" +
                    "Please update your Telegram Bot Token and Chat ID."
                )
                config = self.create_default_config()
                self.update_status("Default configuration created", "orange")
            else:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)

            self.ip_entry.insert(0, config['ip_webcam']['ip_address'])
            self.port_entry.insert(0, config['ip_webcam']['port'])
            self.token_entry.insert(0, config['telegram']['bot_token'])
            self.chatid_entry.insert(0, config['telegram']['chat_id'])
            self.confidence_entry.insert(0, str(config['detection']['confidence_threshold']))
            self.cooldown_entry.insert(0, str(config['detection']['cooldown_seconds']))

            if os.path.exists(self.config_file) and config['telegram']['bot_token'] != "YOUR_BOT_TOKEN_HERE":
                self.update_status("Configuration loaded successfully", "green")
            else:
                self.update_status("Please configure Telegram settings", "orange")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            self.update_status("Failed to load configuration", "red")

    def save_config(self):
        """Save configuration to file"""
        try:
            # Create default config if file doesn't exist
            if not os.path.exists(self.config_file):
                config = self.create_default_config()
            else:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)

            # Update config with current values
            config['ip_webcam']['ip_address'] = self.ip_entry.get()
            config['ip_webcam']['port'] = self.port_entry.get()
            config['telegram']['bot_token'] = self.token_entry.get()
            config['telegram']['chat_id'] = self.chatid_entry.get()
            config['detection']['confidence_threshold'] = float(self.confidence_entry.get())
            config['detection']['cooldown_seconds'] = int(self.cooldown_entry.get())

            # Write updated config
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)

            messagebox.showinfo("Success", "Configuration saved successfully!")
            self.update_status("Configuration saved", "green")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid value entered: {e}\n\nPlease check confidence threshold (0.0-1.0) and cooldown (integer).")
            self.update_status("Invalid configuration values", "red")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            self.update_status("Failed to save configuration", "red")

    def start_detection(self):
        """Start the fall detection system"""
        try:
            # Validate configuration
            if not self.ip_entry.get() or not self.port_entry.get():
                messagebox.showerror("Error", "Please configure IP Webcam settings!")
                return

            if self.token_entry.get() == "YOUR_BOT_TOKEN_HERE" or not self.token_entry.get():
                messagebox.showerror("Error", "Please configure Telegram bot token!")
                return

            if self.chatid_entry.get() == "YOUR_CHAT_ID_HERE" or not self.chatid_entry.get():
                messagebox.showerror("Error", "Please configure Telegram chat ID!")
                return

            # Save current configuration
            self.save_config()

            # Start detection process
            python_exe = sys.executable
            self.process = subprocess.Popen([python_exe, "fall_detection.py"])

            # Update UI
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.update_status("Detection system running...", "#27ae60")

            messagebox.showinfo(
                "System Started",
                "Fall Detection System is now running!\n\n" +
                "The detection window will open shortly.\n" +
                "Press 'q' in the detection window to stop, or use the Stop button."
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start detection: {e}")
            self.update_status("Failed to start", "red")

    def stop_detection(self):
        """Stop the fall detection system"""
        try:
            if self.process:
                self.process.terminate()
                self.process = None

            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.update_status("Detection stopped", "orange")

            messagebox.showinfo("Stopped", "Fall Detection System has been stopped.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop detection: {e}")

    def test_telegram(self):
        """Test Telegram connection"""
        try:
            import requests
            from datetime import datetime

            bot_token = self.token_entry.get()
            chat_id = self.chatid_entry.get()

            if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
                messagebox.showerror("Error", "Please enter your Telegram bot token!")
                return

            if not chat_id or chat_id == "YOUR_CHAT_ID_HERE":
                messagebox.showerror("Error", "Please enter your Telegram chat ID!")
                return

            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': f'✅ Test message from Fall Detection System\n\nTime: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            }

            response = requests.post(url, data=data, timeout=10)

            if response.status_code == 200:
                messagebox.showinfo("Success", "Telegram test message sent successfully!")
                self.update_status("Telegram connection successful", "green")
            else:
                messagebox.showerror("Error", f"Failed to send test message: {response.status_code}")
                self.update_status("Telegram test failed", "red")

        except Exception as e:
            messagebox.showerror("Error", f"Telegram test failed: {e}")
            self.update_status("Telegram test failed", "red")

    def view_logs(self):
        """View log file"""
        log_file = "fall_detection.log"
        if not os.path.exists(log_file):
            messagebox.showinfo("Info", "No log file found. The system hasn't been run yet.")
            return

        # Create log viewer window
        log_window = tk.Toplevel(self.root)
        log_window.title("Fall Detection Logs")
        log_window.geometry("800x600")

        # Text widget with scrollbar
        text_widget = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, font=("Courier", 9))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Read and display log
        with open(log_file, 'r') as f:
            text_widget.insert(tk.END, f.read())

        text_widget.config(state=tk.DISABLED)

        # Refresh button
        def refresh_log():
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            with open(log_file, 'r') as f:
                text_widget.insert(tk.END, f.read())
            text_widget.config(state=tk.DISABLED)

        refresh_btn = tk.Button(log_window, text="Refresh", command=refresh_log)
        refresh_btn.pack(pady=5)

    def open_screenshots(self):
        """Open screenshots folder"""
        screenshots_folder = "fall_screenshots"
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)

        os.startfile(screenshots_folder)

    def update_status(self, message, color="black"):
        """Update status bar"""
        self.status_label.config(text=f"Status: {message}", bg=color if color in ["green", "red", "orange"] else "#34495e")


def main():
    root = tk.Tk()
    app = FallDetectionLauncher(root)

    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
