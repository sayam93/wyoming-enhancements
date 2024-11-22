import subprocess
import time
import logging

MQTT_HOST = "xxx.xxx.xx.xx" # Replace with your Home Assistant IP
MQTT_USER = "user" # Replace with your MQTT user
MQTT_PASSWORD = "password" # Replace with your MQTT password
MQTT_TOPIC = "mqtt/status" # Replace with your own MQTT topic name

def send_mqtt(event_name, message):
    """
    Sends an MQTT message to the configured broker.
    :param event_name: Event name (e.g., "status").
    :param message: Message payload (e.g., "connected", "disconnected").
    """
    try:
        logging.info(f"Sending MQTT message: {event_name} - {message}")
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
            check=True,  # Raise exception if the command fails
        )
        logging.info("MQTT message sent successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to send MQTT message: {e}")
    except Exception as e:
        logging.exception("Unexpected exception in send_mqtt")

if __name__ == "__main__":
    # Sends a "disconnected" payload on script execution
    event_name = "status"
    message = "disconnected"
    send_mqtt(event_name, message)