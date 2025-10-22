"""
Human Fall Detection System
Uses MediaPipe Pose Estimation and IP Webcam to detect falls
Sends alerts to Telegram with screenshots
"""

import cv2
import mediapipe as mp
import numpy as np
import requests
import json
import time
import logging
from datetime import datetime
import os
from pathlib import Path


class FallDetectionSystem:
    def __init__(self, config_path='config.json'):
        """Initialize the fall detection system"""
        # Load configuration
        self.config = self.load_config(config_path)

        # Setup logging
        self.setup_logging()

        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=self.config['detection']['min_detection_confidence'],
            min_tracking_confidence=self.config['detection']['min_detection_confidence']
        )

        # Fall detection parameters
        self.fall_angle_threshold = self.config['detection']['fall_angle_threshold']
        self.confidence_threshold = self.config['detection']['confidence_threshold']
        self.cooldown_seconds = self.config['detection']['cooldown_seconds']

        # State management
        self.last_alert_time = 0
        self.fall_detected = False

        # Create screenshots folder
        self.screenshots_folder = Path(self.config['system']['screenshots_folder'])
        self.screenshots_folder.mkdir(exist_ok=True)

        # Webcam URL
        self.webcam_url = f"http://{self.config['ip_webcam']['ip_address']}:{self.config['ip_webcam']['port']}{self.config['ip_webcam']['stream_path']}"

        logging.info("Fall Detection System initialized")
        logging.info(f"Webcam URL: {self.webcam_url}")

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Config file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in config file: {config_path}")
            raise

    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.config['system']['log_file']
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

    def calculate_angle(self, point1, point2):
        """Calculate angle between two points relative to horizontal"""
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        angle = abs(np.degrees(np.arctan2(dy, dx)))
        return angle

    def detect_fall(self, landmarks, image_height, image_width):
        """
        Detect fall based on pose landmarks
        Returns: (is_fall, confidence, details)
        """
        try:
            # Get key body landmarks
            left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]

            # Calculate center points
            shoulder_center = [
                (left_shoulder.x + right_shoulder.x) / 2,
                (left_shoulder.y + right_shoulder.y) / 2
            ]
            hip_center = [
                (left_hip.x + left_hip.x) / 2,
                (left_hip.y + right_hip.y) / 2
            ]

            # Calculate body angle (shoulder to hip)
            body_angle = self.calculate_angle(shoulder_center, hip_center)

            # Calculate vertical position (normalized)
            avg_y_position = (shoulder_center[1] + hip_center[1]) / 2

            # Fall detection logic
            # 1. Body is nearly horizontal (angle close to 0 or 180)
            is_horizontal = body_angle < self.fall_angle_threshold or body_angle > (180 - self.fall_angle_threshold)

            # 2. Person is in lower part of frame (fallen down)
            is_low_position = avg_y_position > 0.6  # Lower 40% of frame

            # 3. Shoulder and hip are at similar height (lying down)
            height_diff = abs(shoulder_center[1] - hip_center[1])
            is_flat = height_diff < 0.15

            # Combine conditions
            is_fall = is_horizontal and (is_low_position or is_flat)

            # Calculate confidence based on how well conditions are met
            confidence = 0.0
            if is_horizontal:
                confidence += 0.4
            if is_low_position:
                confidence += 0.3
            if is_flat:
                confidence += 0.3

            details = {
                'body_angle': body_angle,
                'y_position': avg_y_position,
                'height_diff': height_diff,
                'is_horizontal': is_horizontal,
                'is_low_position': is_low_position,
                'is_flat': is_flat
            }

            return is_fall, confidence, details

        except Exception as e:
            logging.error(f"Error in fall detection: {e}")
            return False, 0.0, {}

    def send_telegram_alert(self, image, details):
        """Send alert to Telegram with screenshot"""
        try:
            # Save screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.screenshots_folder / f"fall_{timestamp}.jpg"
            cv2.imwrite(str(screenshot_path), image, [cv2.IMWRITE_JPEG_QUALITY, self.config['system']['screenshot_quality']])

            # Prepare message
            message = f"🚨 FALL DETECTED 🚨\n\n"
            message += f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            message += f"📊 Confidence: {details.get('confidence', 0):.2%}\n"
            message += f"📐 Body Angle: {details.get('body_angle', 0):.1f}°\n"
            message += f"📍 Position: {details.get('y_position', 0):.2f}"

            # Send message
            bot_token = self.config['telegram']['bot_token']
            chat_id = self.config['telegram']['chat_id']

            # Send text message
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message
            }
            response = requests.post(url, data=data, timeout=10)

            # Send photo
            url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            with open(screenshot_path, 'rb') as photo:
                files = {'photo': photo}
                data = {'chat_id': chat_id}
                response = requests.post(url, data=data, files=files, timeout=10)

            if response.status_code == 200:
                logging.info(f"Alert sent successfully. Screenshot saved: {screenshot_path}")
                return True
            else:
                logging.error(f"Failed to send alert: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logging.error(f"Error sending Telegram alert: {e}")
            return False

    def test_telegram(self):
        """Test Telegram connection"""
        try:
            bot_token = self.config['telegram']['bot_token']
            chat_id = self.config['telegram']['chat_id']

            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': '✅ Fall Detection System - Connection Test Successful!\n\n' +
                        f'System is ready and monitoring.\n' +
                        f'Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            }
            response = requests.post(url, data=data, timeout=10)

            if response.status_code == 200:
                logging.info("Telegram test successful")
                return True
            else:
                logging.error(f"Telegram test failed: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"Telegram test error: {e}")
            return False

    def run(self):
        """Main loop for fall detection"""
        logging.info("Starting fall detection system...")

        # Test Telegram connection
        print("\n🔄 Testing Telegram connection...")
        if self.test_telegram():
            print("✅ Telegram connection successful!\n")
        else:
            print("❌ Telegram connection failed! Check your bot token and chat ID.\n")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return

        # Connect to IP Webcam
        print(f"🔄 Connecting to IP Webcam at {self.webcam_url}...")
        cap = cv2.VideoCapture(self.webcam_url)

        if not cap.isOpened():
            logging.error("Failed to connect to IP Webcam")
            print("❌ Failed to connect to IP Webcam!")
            print("Make sure:")
            print("  1. IP Webcam app is running on your phone")
            print("  2. Your phone and computer are on the same network")
            print(f"  3. The IP address {self.config['ip_webcam']['ip_address']} is correct")
            return

        print("✅ Connected to IP Webcam!")
        print("\n" + "="*50)
        print("Fall Detection System is now ACTIVE")
        print("="*50)
        print("Press 'q' to quit")
        print("Press 't' to test alert")
        print("="*50 + "\n")

        frame_count = 0
        fps_target = self.config['system']['fps']

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logging.warning("Failed to read frame")
                    time.sleep(1)
                    continue

                frame_count += 1

                # Process every frame based on FPS setting
                if frame_count % (30 // fps_target) != 0:
                    continue

                # Convert to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process pose
                results = self.pose.process(rgb_frame)

                # Draw pose landmarks
                if results.pose_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS
                    )

                    # Detect fall
                    landmarks = results.pose_landmarks.landmark
                    is_fall, confidence, details = self.detect_fall(
                        landmarks,
                        frame.shape[0],
                        frame.shape[1]
                    )

                    # Check if fall detected and confidence is high enough
                    if is_fall and confidence >= self.confidence_threshold:
                        current_time = time.time()

                        # Check cooldown
                        if current_time - self.last_alert_time >= self.cooldown_seconds:
                            logging.warning(f"FALL DETECTED! Confidence: {confidence:.2%}")
                            details['confidence'] = confidence

                            # Send alert
                            if self.send_telegram_alert(frame, details):
                                self.last_alert_time = current_time
                                print(f"\n🚨 FALL DETECTED! Alert sent at {datetime.now().strftime('%H:%M:%S')}")
                                print(f"   Confidence: {confidence:.2%}")
                                print(f"   Next alert available in {self.cooldown_seconds} seconds\n")
                        else:
                            remaining = int(self.cooldown_seconds - (current_time - self.last_alert_time))
                            cv2.putText(frame, f"Cooldown: {remaining}s", (10, 30),
                                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                    # Display status
                    status = "FALL DETECTED!" if is_fall else "Monitoring"
                    color = (0, 0, 255) if is_fall else (0, 255, 0)
                    cv2.putText(frame, status, (10, 60),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                    cv2.putText(frame, f"Conf: {confidence:.2%}", (10, 90),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                # Display frame
                cv2.imshow('Fall Detection System', frame)

                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n👋 Shutting down...")
                    break
                elif key == ord('t'):
                    print("\n🧪 Sending test alert...")
                    test_details = {
                        'confidence': 1.0,
                        'body_angle': 0,
                        'y_position': 0.8
                    }
                    if self.send_telegram_alert(frame, test_details):
                        print("✅ Test alert sent successfully!\n")
                    else:
                        print("❌ Failed to send test alert!\n")

        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")

        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.pose.close()
            logging.info("Fall detection system stopped")
            print("✅ System stopped successfully")


def main():
    """Main entry point"""
    print("\n" + "="*50)
    print("Human Fall Detection System")
    print("="*50 + "\n")

    try:
        detector = FallDetectionSystem('config.json')
        detector.run()
    except FileNotFoundError:
        print("❌ Error: config.json not found!")
        print("Please make sure config.json exists in the same folder.")
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"Fatal error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
