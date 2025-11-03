import subprocess
import threading
import os

# Get the current directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define script paths using os.path.join
HEAD_SCRIPT = os.path.join(CURRENT_DIR, "cc4.py")
GPS_SCRIPT = os.path.join(CURRENT_DIR, "maxgforce.py")
TRAFFIC_LIGHT_SCRIPT = os.path.join(CURRENT_DIR, "trafficlight.py")
RAIN_SCRIPT = os.path.join(CURRENT_DIR, "rain.py")

def run_script(script_path):
    """Run a Python script as a subprocess."""
    try:
        subprocess.Popen(["lxterminal", "-e", f"python3 {script_path}"])
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")

if __name__ == "__main__":
    # Create threads for each script
    head_thread = threading.Thread(target=run_script, args=(HEAD_SCRIPT,))
    gps_thread = threading.Thread(target=run_script, args=(GPS_SCRIPT,))
    traffic_light_thread = threading.Thread(target=run_script, args=(TRAFFIC_LIGHT_SCRIPT,))
    rain_thread = threading.Thread(target=run_script, args=(RAIN_SCRIPT,))

    # Start all scripts simultaneously
    head_thread.start()
    gps_thread.start()
    traffic_light_thread.start()
    rain_thread.start()

    # Wait for all scripts to finish (optional)
    head_thread.join()
    gps_thread.join()
    traffic_light_thread.join()
    rain_thread.join()

    print("All scripts have finished execution.")
