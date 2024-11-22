import RPi.GPIO as GPIO
import time
import subprocess
import logging

MQTT_HOST = "xxx.xxx.xx.xx" # Replace with your Home Assistant IP
MQTT_USER = "user" # Replace with your MQTT user
MQTT_PASSWORD = "password" # Replace with your MQTT password
MQTT_TOPIC = "mqtt/status" # Replace with your own MQTT topic name
BUTTON_PIN = 17  # GPIO pin for the button

def send_mqtt(message):
    """
    Sends an MQTT message to the Home Assistant.
    :param message: Message payload (e.g., "on", "off").
    """
    try:
        logging.info(f"Sending MQTT message: {message}")
        subprocess.run(
            [
                "mosquitto_pub",
                "-t", MQTT_TOPIC,
                "-h", MQTT_HOST,
                "-m", message,
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

def setup_gpio():
    """
    Configures the GPIO pin for the button.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN)

def main():
    """
    Main loop to monitor button state and send MQTT messages.
    """
    setup_gpio()
    logging.info("Monitoring button state...")
    try:
        while True:
            state = GPIO.input(BUTTON_PIN)
            if state:
                send_mqtt("off")
            else:
                send_mqtt("on")
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Exiting on user interrupt.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()