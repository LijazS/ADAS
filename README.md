# Advanced Driver Support System (ADSS)
Department of Computer Science and Engineering | College of Engineering Thalassery

## Project Overview
The Advanced Driver Support System is an AI-powered device designed to enhance driving safety and convenience using a Raspberry Pi 5B. This system addresses critical road safety challenges such as headlight glare, accident detection, and lack of real-time incident documentation. By integrating computer vision and sensor data, ADSS provides an intuitive and automated driving assistance experience.

## Key Features

**Automatic Headlight Beam Controller:** Dynamically switches between high and low beams based on oncoming traffic to reduce glare.

**Intelligent Dashcam:** Continuous footage recording with a GUI for date/time-specific playback.

**Accident Detection System:** Monitors G-force in real-time to detect impacts or free falls.

**Emergency Video Reporting:** Automatically extracts footage from the moment of an accident and emails it to emergency contacts.

**Traffic Light Approach Alert:** Uses GPS to warn drivers if they are over-speeding (>60 km/h) while approaching a traffic light.

## Hardware & Tech Stack

### Hardware Components
- **Microcontroller:** Raspberry Pi 5B (Chosen for integrated GPU and fast processing).
- **Vision:** Camera Module.
- **Sensors:** MPU6050 Accelerometer/Gyroscope, Neo 6M GPS Module.
- **Power:** 5V Buck Converter (converts car 12V to 5V 5A).
- **Actuators:** Relay Circuit (for headlight control).

### Software Libraries
- OpenCV (Image Processing)
- Yagmail (Automated Emailing)
- Threading (Concurrency)
- Tkinter (GUI for Dashcam)

## Modules and Implementation

### 1. Headlight Detection & Control

**How it works:**  
The system captures video frames, converts them to grayscale, and applies a trapezoid-shaped mask to focus on the road. It blurs the image to reduce noise and detects bright contours (oncoming headlights). If a bright light is detected, the system warns the driver or dims the lights.

<p align="center">
<img src="images/1.png" alt="Headlight Detection Output" width="600">
</p>

**Challenges & Solutions:**  
- **Problem:** Street lights and shop lights caused false detections.  
  **Solution:** Implemented a Region of Interest (ROI) mask and brightness thresholds. If the ambient area is generally too bright, high beams are kept off.

- **Problem:** High memory usage and processing lag.  
  **Solution:** Lowered resolution and converted frames to Black & White to speed up processing.

---

### 2. Dashcam System

**How it works:**  
The system continuously saves frames. A custom GUI allows the user to select a specific date and time range ("From" and "To") to view the recorded footage as a video.

<p align="center">
<img src="images/2.png" alt="Dashcam User Interface" width="400">
<img src="images/2.1.png" alt="Dashcam User Interface" width="400">
</p>

**Challenges & Solutions:**  
- **Problem:** Simultaneous video detection and converting frames to MP4 formats like .mp4 was too resource-intensive for the Pi.  
  **Solution:** Frames are saved as individual images instead of a video file. Multi-threading is used to handle saving in the background without freezing the detection loop.

---

### 3. Accident Detection & Reporting

**How it works:**  
Using the MPU6050 sensor via I2C communication, the system calculates the total G-force using the formula:

$$g_{total} = \sqrt{g_x^2 + g_y^2 + g_z^2}$$


**Severity Thresholds:**  
- 5–20g: Mild Accident  
- 30–40g: Medium Accident  
- 50g+: Severe Accident  

If an accident is detected, the system extracts footage starting from 3 minutes prior to the incident, compiles it, and sends it via email.

<p align="center">
<img src="images/3.png" alt="Accident Detection Logic" width="500">
</p>

---

### 4. Traffic Light & Speed Monitoring

**How it works:**  
The system loads a database of traffic light coordinates (traffic_lights.txt). It continuously compares the vehicle's live GPS location with these coordinates. If the vehicle is within 300 meters of a light and the speed exceeds 60 km/h, an alert is triggered.

<p align="center">
<img src="images/4.png" alt="Traffic Light Detection Terminal" width="600">
</p>

---

## Circuit Diagrams

### Internal Connections
The Raspberry Pi acts as the central hub connecting the Camera, Accelerometer, GPS, and Relay.

 <p align="center">
<img src="images/5.png" alt="Internal Circuit Diagram" width="600">
<img src="images/5.1.png" alt="Internal Circuit Diagram" width="600">
</p>

### External Wiring
Shows the connection between the 12V Car Battery, the Buck Converter, the Relay, and the Headlights.
 <p align="center"> 
<img src="images/6.png" alt="External Wiring Diagram" width="600">
</p>

---

## Future Scope
- Smart Dashboard: Touchscreen interface with OBD-II diagnostics  
- Security: Motion detection alerts when the car is parked  
- Automation: Voice commands and remote engine start  
- Connectivity: Car-to-Home IoT integration  

---

## Team Members
- Lijaz Salim  
- Mohammed Fadil  
- Nilofer Nissar C  
- Wafa Nahas  

**Guide:** Asst Prof. T V Rashma
