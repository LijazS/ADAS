import cv2
from picamera2 import Picamera2

class DashCam:
    def __init__(self, width=640, height=480):
        self.cap = Picamera2()
        # Configure video with the specified resolution
        self.cap.configure(
            self.cap.create_video_configuration(main={"format": "RGB888", "size": (width, height)})
        )
        # Set camera controls (adjust as needed)
        self.cap.set_controls({
            "AfMode": 1,  # Auto-focus mode
            "ExposureValue": -1.5,
        })
        self.cap.start()  # Start the camera

    def get_frame(self):
        frame = self.cap.capture_array()  # Capture a frame
        frame = cv2.flip(frame, -1)  # Flip the frame vertically
        return frame

    def release(self):
        self.cap.stop()  # Stop capturing from the camera
        cv2.destroyAllWindows()  # Close any OpenCV windows
