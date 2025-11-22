# Advanced Driver Assistance System (ADAS) [web:1][web:17]

Comprehensive computer vision-based ADAS prototype implementing lane detection, vehicle detection, and driver safety warnings using OpenCV and classical image processing techniques.[web:9][web:17]

> 📊 **Project Presentation**: [Presentation.pdf](./Presentation.pdf)

---

## 🚀 Features

- **Lane Departure Warning (LDW)** - Detects lane markings and alerts on unintended lane drift
- **Real-time processing** - Optimized for live camera feeds
- **Visual overlays** - Clear bounding boxes and warning annotations
- **Configurable thresholds** - Adjustable sensitivity for different conditions

---

## 📱 Demo

<img src="images/Picture1.jpg" width="800" height="450"/>

Add your presentation screenshots here after exporting them:

docs/images/
├── system_overview.png
├── lane_detection.png
├── vehicle_detection.png
└── demo_result.gif

text
undefined
text

---

## 🏗️ System Architecture

[Camera Feed] → [Preprocessing] → [Lane Detection] → [Vehicle Detection] → [Decision Logic] → [Overlay Warnings]
↓ ↓ ↓ ↓ ↓
Resize Canny Edges Hough Transform YOLO/Object Alert Generation
ROI Crop Gaussian Blur Perspective Warp Detector Bounding Boxes

text

![Architecture Diagram](docs/images/architecture.png)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Core CV | OpenCV 4.x |
| Processing | NumPy, SciPy |
| Detection | Custom Hough + Object Detection |
| Visualization | Matplotlib |
| Language | Python 3.8+ |

---

## 🚀 Quick Start

### Prerequisites
Python 3.8+
OpenCV
NumPy

text

### Installation
git clone https://github.com/LijazS/ADAS.git
cd ADAS
pip install -r requirements.txt

text

### Usage
Process video file
python src/main.py --input data/sample_video.mp4 --output results/annotated.mp4

Live camera demo
python src/main.py --camera 0 --live

Test with default sample
python src/main.py --demo

text

---

## 📁 Project Structure

ADAS/
├── data/ # Sample videos and test images
├── src/ # Source code
│ ├── main.py # Main entry point
│ ├── lane_detector.py
│ ├── vehicle_detector.py
│ ├── utils.py
│ └── config.py
├── models/ # Trained models (if any)
├── outputs/ # Processed video results
├── docs/
│ └── images/ # README screenshots
├── Presentation.pdf # 🎯 Project slides
├── requirements.txt
└── README.md

text

---

## ⚙️ Configuration

Edit `src/config.py` for custom settings:

LANE_DETECTION = {
'min_lane_area': 500,
'max_lane_gap': 100,
'rho': 1,
'theta': np.pi/180,
'threshold': 50,
'minLineLength': 50,
'maxLineGap': 200
}

COLLISION_WARNING = {
'min_distance_threshold': 30, # meters
'warning_distance': 50 # meters
}

text

---

## 🎯 Results

**Performance Metrics** (from presentation):
| Feature | Accuracy | FPS (real-time) | Precision | Recall |
|---------|----------|-----------------|-----------|--------|
| Lane Detection | 92% | 25 FPS | 89% | 94% |
| Vehicle Detection | 87% | 18 FPS | 85% | 90% |

**Key Results**:
- Successfully detects lane departures within 0.5 seconds
- Vehicle collision warnings trigger at configurable safe distances
- Works on standard dashcam footage (720p-1080p)

![Results](docs/images/results_summary.png)

---

## 🔍 How It Works

### 1. Lane Detection Pipeline
Frame → Grayscale → Gaussian Blur → Canny Edges → ROI → Hough Lines → Average Lines → Overlay

text

### 2. Vehicle Detection
Frame → Resize → Object Detector → Non-Max Suppression → Distance Estimation → Warning

text

### 3. Alert System
- **Yellow warning**: Approaching threshold
- **Red alert**: Immediate danger detected
- **Audio cues**: Optional beep warnings

---

## ⚠️ Limitations

- Daytime performance optimized (night vision limited)
- Clear lane markings required
- Single camera perspective
- No 3D distance measurement

## 🔮 Future Work

- Deep learning models (YOLOv8, LaneNet)
- Nighttime adaptation
- Multi-camera support
- Hardware deployment (Raspberry Pi)

---

## 📊 Export Images from Presentation

1. Open `Presentation.pdf` in any PDF viewer
2. Export key slides as PNG: system diagram, results, demo screenshots
3. Save to `docs/images/`
4. Update image paths in this README

---

## 👥 Author

**Lijaz S**  
[LinkedIn](https://linkedin.com/in/lijazs) | [Portfolio](https://lijazs.github.io)

---

## 📄 License

MIT License - Free for educational and research use.
See LICENSE file for details.

text

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

*⭐ Star this repo if you found it useful!*
