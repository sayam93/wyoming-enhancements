import subprocess
import logging
import datetime
import os

# MQTT configuration
MQTT_HOST = "xxx.xxx.xx.xx" # Replace with your Home Assistant IP
MQTT_USER = "user" # Replace with your MQTT user
MQTT_PASSWORD = "password" # Replace with your MQTT password
MQTT_TOPIC = "mqtt/status" # Replace with your own MQTT topic name

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def log_message(message):
    """Log a message with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{timestamp} [detected.py] {message}")

def speak(message):
    """Uses the espeak utility to speak a message."""
    try:
        subprocess.run(["espeak", message], check=True)
        log_message(f"Spoken message: {message}")
    except FileNotFoundError:
        logging.error("espeak not found. Please install espeak.")
    except Exception as e:
        logging.error(f"Error speaking message: {e}")

def start_audio_ducking():
    """Start the audio ducking process."""
    try:
        log_message("Starting silence process...")
        subprocess.Popen(
            [
                "pacat",
                "--client-name=silence",
                "--volume=0",
                "--property=media.role=notification",
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        log_message("Silence process started.")
    except FileNotFoundError:
        logging.error("pacat not found. Please install PulseAudio.")
    except Exception as e:
        logging.error(f"Error starting silence process: {e}")

def send_mqtt(event_name, message):
    """
    Sends an MQTT message to the configured broker.
    :param event_name: Event name (e.g., "status").
    :param message: Message payload (e.g., "detected").
    """
    try:
        log_message(f"Sending MQTT message: {event_name} - {message}")
        subprocess.run(
            [
                "mosquitto_pub",
                "-t", MQTT_TOPIC,
                "-h", MQTT_HOST,
                "-m", f"{event_name}: {message}",
                "-u", MQTT_USER,
                "-P", MQTT_PASSWORD,
            ],
            text=True,
            check=True,
        )
        log_message("MQTT message sent successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to send MQTT message: {e}")
    except Exception as e:
        logging.exception("Unexpected exception in send_mqtt")

if __name__ == "__main__":
    log_message("Starting detected.py script...")

    # Speak a message
    speak("How may I help you?")

    # Start audio ducking
    start_audio_ducking()

    # Send MQTT message
    send_mqtt("status", "detected")

    log_message("detected.py script complete.")