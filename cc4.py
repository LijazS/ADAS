import cv2
import numpy as np
import time
from datetime import datetime
import os
import threading
import queue
from cam import DashCam  # Import DashCam from cam.py

# Global variables
brightness_threshold = 125  # Brightness threshold for small contour region
small_contour_area_threshold_min = 100  # Minimum threshold for small contour area
small_contour_area_threshold_max = 5000  # Maximum threshold for small contour area
visualize_roi = True  # Enable ROI and contour visualization
output_folder = "saved_frames"
last_detection_time = 0  # Variable to track last detection time
detection_cooldown = 1  # Cooldown time in seconds for the detection message

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

frame_queue = queue.Queue()

# Thread to save frames
def save_frames():
    frame_count = 0
    while True:
        frame = frame_queue.get()
        if frame is None:
            break
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
        frame_filename = os.path.join(output_folder, f"frame_{timestamp}.png")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1
        frame_queue.task_done()

save_thread = threading.Thread(target=save_frames, daemon=True)
save_thread.start()

# Scenario processing function
def scenario(frame_resized):
    global brightness_threshold, small_contour_area_threshold_min, small_contour_area_threshold_max, last_detection_time, detection_cooldown

    # Resize the frame for processing
    scale_factor = 0.5  # Define scale factor here (adjust as needed)
    frame_resized = cv2.resize(frame_resized, (0, 0), fx=scale_factor, fy=scale_factor)

    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    height, width = frame_resized.shape[:2]

    # Define trapezoid ROI
    trapezoid_height = int(0.20 * height)
    top_width_ratio = 0.5
    top_center_x = width // 2
    top_left = (int(top_center_x - (top_width_ratio * width) / 10), height - trapezoid_height)
    top_right = (int(top_center_x + (top_width_ratio * width) / 1.5), height - trapezoid_height)
    bottom_left = (0, height)
    bottom_right = (width, height)

    mask = np.zeros((height, width), dtype=np.uint8)
    trapezoid_points = np.array([bottom_left, bottom_right, top_right, top_left], dtype=np.int32)
    cv2.fillPoly(mask, [trapezoid_points], 255)

    masked_frame = cv2.bitwise_and(frame_resized, frame_resized, mask=mask)
    gray_image = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)

    # Blur and threshold the image
    blur_image = cv2.blur(gray_image, (5, 5))
    _, thresh = cv2.threshold(blur_image, 150, 255, 0)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if visualize_roi:
        cv2.polylines(frame_resized, [trapezoid_points], isClosed=True, color=(0, 255, 255), thickness=2)

    detection_message = "Headlight NOT Detected"
    color = (0, 0, 255)  # Default: Red for "Not Detected"
    headlight_detected = False

    # Process contours
    for cnt in contours:
        contour_area = cv2.contourArea(cnt)

        # Only process contours within the specified area range
        if small_contour_area_threshold_min < contour_area < small_contour_area_threshold_max:
            # Calculate brightness in the contour's bounding box
            x, y, w, h = cv2.boundingRect(cnt)
            contour_region = gray_image[y:y+h, x:x+w]
            avg_brightness = np.mean(contour_region)

            if avg_brightness > brightness_threshold:
                headlight_detected = True
                last_detection_time = time.time()  # Update last detection time
                if visualize_roi:
                    cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Check if we need to show "Headlight Detected" for an extra second after the headlight goes away
    current_time = time.time()
    if headlight_detected or (current_time - last_detection_time <= detection_cooldown):
        detection_message = "Headlight Detected"
        color = (0, 255, 0)  # Green for "Detected"
    else:
        detection_message = "Headlight NOT Detected"
        color = (0, 0, 255)  # Red for "Not Detected"

    # Display the message
    cv2.putText(frame_resized, detection_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    return frame_resized

# Initialize DashCam
dash_cam = DashCam()

try:
    while True:
        frame = dash_cam.get_frame()
        if frame is None:
            print("Error: Unable to fetch frame from DashCam.")
            break

        processed_frame = scenario(frame)
        frame_queue.put(frame)
        cv2.imshow("Processed Frame", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    frame_queue.put(None)
    frame_queue.join()
    dash_cam.release()
