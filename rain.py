import RPi.GPIO as GPIO
import time

RAIN_SENSOR_PIN = 17  # Using GPIO17 (Pin 11)

GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(RAIN_SENSOR_PIN) == 0:  # Assuming LOW means water detected
            print("Water Detected!")
        time.sleep(1)  # Delay to avoid too many prints

except KeyboardInterrupt:
    GPIO.cleanup()