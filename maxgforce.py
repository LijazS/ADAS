import smbus
import math
import time
import os
import yagmail

accident = 0
mild = 0
moderate = 0
severe = 0
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# MPU6050 Registers and their Address
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F

# Initialize the MPU6050 sensor
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)  # Wake up the MPU6050

def convert_latest_images_to_video(folder_path, output_video="output.avi", max_images=1500, fps=30):
    """Get the latest max_images from the folder and convert them into a video."""
    folder_path = os.path.abspath(folder_path)
    output_video = os.path.abspath(output_video)

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return None
    
    images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".png")]
    images.sort(key=os.path.getctime, reverse=False)  # Sort by creation time (latest first)
    image_files = images[:max_images]

    if not image_files:
        print("No images found.")
        return None

    frame = cv2.imread(image_files[0])
    if frame is None:
        print("Error: Could not read the first image.")
        return None

    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    print("Converting images to video...")

    for img in image_files:
        frame = cv2.imread(img)
        if frame is not None:
            video.write(frame)

    video.release()
    print("Video conversion finished! Saved as:", output_video)
    return output_video

def send_email_with_attachment_yagmail(attachment, sender_email, sender_password, recipient_email,coords):
    try:
        yag = yagmail.SMTP(sender_email, sender_password)
        yag.send(
            to=recipient_email,
            subject="EMERGENCY",
            contents=f"Emergency, an accident has occured on {coords}video is attached",
            attachments=attachment
        )
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def read_raw_data(addr):
    """Read two bytes of raw data from the given address."""
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = (high << 8) | low
    if value > 32768:
        value -= 65536
    return value

def get_g_force():
    """Calculate the current g-force on each axis and total g-force."""
    accel_x = read_raw_data(ACCEL_XOUT_H)
    accel_y = read_raw_data(ACCEL_YOUT_H)
    accel_z = read_raw_data(ACCEL_ZOUT_H)

    # Sensitivity scale factor for accelerometer (+/- 2g)
    accel_x_g = accel_x / 16384.0
    accel_y_g = accel_y / 16384.0
    accel_z_g = accel_z / 16384.0

    # Calculate the total g-force
    total_g = math.sqrt(accel_x_g**2 + accel_y_g**2 + accel_z_g**2)

    return total_g

def main():
    max_g_force = 0.0
    min_g_force = float('inf')  # Set initial minimum to infinity
    last_print_time = time.time()

    print("Reading g-force from MPU6050. Press Ctrl+C to stop.")

    try:
        while True:
            current_g = get_g_force()
            
            # Check if the g-force excceed threshhold
            if 5 <= current_g <= 29:
                mild = 1
                accident = 1
            elif 30 <= current_g <= 49:
                moderate = 1
                accident = 1
            elif 50 <= current_g <= 1000:
                severe = 1
                accident = 1
            else:
                accident = 0
                mild = 0
                moderate = 0
                severe = 0
                
             # If an accident is detected, trigger video and email functions
            if accident:
                folder_path = os.path.join(CURRENT_DIR, "footages")
                output_video = os.path.join(CURRENT_DIR, "footages/latest_emergency_video.avi")
                sender_email = "jumboproject45@gmail.com"
                sender_password = "zrbi imnn ddhv isho"
                recipient_email = "lijazsalim@gmail.com"
                coords_file = COORDS_FILE = os.path.join(os.path.dirname(__file__), "cords.txt")
                
                with open(coords_file, "r") as file:
                    coords = file.read().strip() or "12.295494683718717, 75.30756144747816"  

                
                video_file = convert_latest_images_to_video(folder_path, output_video)
                if video_file:
                    send_email_with_attachment_yagmail(video_file, sender_email, sender_password, recipient_email,coords)


            # Update maximum and minimum g-force
            max_g_force = max(max_g_force, current_g)
            min_g_force = min(min_g_force, current_g)

            # Print the values with a 1-second delay at the current moment
            current_time = time.time()
            if current_time - last_print_time >= 1.0:
                print(f"Current g-force: {current_g:.2f}g, Maximum: {max_g_force:.2f}g, Minimum: {min_g_force:.2f}g")
                last_print_time = current_time  # Update the print time

            time.sleep(0.1)  # Keep the loop running faster for accuracy

    except KeyboardInterrupt:
        print("\nProgram stopped.")

if __name__ == "__main__":
    main()
