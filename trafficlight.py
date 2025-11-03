import serial
import pynmea2
from geopy.distance import geodesic
import time
import os

# Configuration
GPS_PORT = '/dev/ttyAMA0'  # Default UART port for Raspberry Pi
BAUD_RATE = 9600  # Standard for Neo 6M
GPS_TIMEOUT = 10  # Max wait time for a GPS fix (seconds)
RADIUS_KM = 0.3  # Detection radius (300 meters)
SPEED_LIMIT_KPH = 60  # Speed limit
COORDS_FILE = os.path.join(os.path.dirname(__file__), "cords.txt")  # File to store live coordinates

# Load traffic light coordinates from a file
def load_traffic_light_coords(file_path):
    try:
        with open(file_path, 'r') as file:
            return [tuple(map(float, line.strip().split(','))) for line in file]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

# Read a single GPS sentence
def read_gps_sentence(gps_serial):
    try:
        return gps_serial.readline().decode('utf-8', errors='ignore').strip()
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None

# Fetch GPS data with a timeout
def get_gps_data():
    try:
        with serial.Serial(GPS_PORT, BAUD_RATE, timeout=1) as gps_serial:
            start_time = time.time()
            while time.time() - start_time < GPS_TIMEOUT:
                sentence = read_gps_sentence(gps_serial)
                if sentence and sentence.startswith(('$GPGGA', '$GPRMC')):
                    try:
                        return pynmea2.parse(sentence)
                    except pynmea2.ParseError:
                        pass  # Ignore corrupt sentences
                time.sleep(0.1)  # Reduce CPU usage
        print("Timeout: No valid GPS signal.")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    return None

# Check if near a traffic light
def is_near_traffic_light(current_coords, traffic_light_coords):
    for tl_coord in traffic_light_coords:
        if geodesic(current_coords, tl_coord).km <= RADIUS_KM:
            return tl_coord
    return None

# Get speed from parsed GPS data
def get_speed_kph(parsed_data):
    if hasattr(parsed_data, 'spd_over_grnd') and parsed_data.spd_over_grnd is not None:
        return parsed_data.spd_over_grnd * 1.852  # Convert knots to km/h
    return None

# Write live coordinates to a text file
def write_live_coords(coords):
    try:
        with open(COORDS_FILE, 'w') as file:  # Overwrite with latest data
            file.write(f"{coords[0]},{coords[1]}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Main loop
if __name__ == "__main__":
    traffic_light_coords = load_traffic_light_coords('traffic_lights.txt')

    if not traffic_light_coords:
        print("No traffic light data. Exiting.")
        exit(1)

    print("Tracking... Press Ctrl+C to stop.")

    try:
        while True:
            parsed_data = get_gps_data()
            if parsed_data and hasattr(parsed_data, 'latitude') and hasattr(parsed_data, 'longitude'):
                current_coords = (parsed_data.latitude, parsed_data.longitude)
                print(f"Location: {current_coords}")

                # Write live coordinates to file
                write_live_coords(current_coords)

                # Check traffic light proximity
                near_light = is_near_traffic_light(current_coords, traffic_light_coords)
                if near_light:
                    print(f"🚦 Near traffic light: {near_light}")

                    # Check speed
                    speed = get_speed_kph(parsed_data)
                    if speed is not None:
                        if speed > SPEED_LIMIT_KPH:
                            print(f"⚠️ Overspeeding! {speed:.2f} km/h (Slow down!)")
                        else:
                            print(f"✅ Speed: {speed:.2f} km/h (Within limit)")
                else:
                    print("No traffic lights nearby.")
            time.sleep(1)  # Optimize CPU usage
    except KeyboardInterrupt:
        print("\nExiting program.")
