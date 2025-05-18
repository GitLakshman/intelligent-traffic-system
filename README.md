# Traffic Density Based Signal Timing Control System 🚦

This project implements an intelligent traffic signal control system that dynamically adjusts signal timings based on real-time traffic density. Using Raspberry Pi and computer vision techniques, the system aims to optimize vehicle flow, reduce congestion, and contribute to smarter urban traffic management.

## 📌 Project Overview

Traditional fixed-timing traffic signals often lead to unnecessary delays and congestion. This project uses a CCTV camera and the YOLO object detection model to monitor traffic density and adjust green signal durations accordingly.

## 🛠️ Technologies & Components

- **Hardware:**
  - Raspberry Pi 3 Model B
  - USB/CCTV Camera
  - LED traffic signal simulation
  - Regulated power supply

- **Software:**
  - Python 3
  - OpenCV
  - YOLO (You Only Look Once) for object detection
  - Raspberry Pi OS
  - Thonny IDE / VS Code

## 🧠 Key Features

- Real-time vehicle detection using YOLOv3 model
- Dynamic traffic signal timing based on lane-wise vehicle count
- GPIO control of LEDs to simulate traffic signals
- Image preprocessing for enhanced accuracy
- Power-efficient and cost-effective design
- Scalable solution for smart city applications

## ⚙️ How It Works

1. **Capture:** Camera continuously captures traffic images.
2. **Detect:** YOLO model detects and counts vehicles in each lane.
3. **Analyze:** Vehicle count is used to calculate optimal green time.
4. **Control:** Raspberry Pi adjusts LED traffic lights via GPIO pins.
5. **Loop:** Process repeats to adapt to real-time conditions.

## 📷 Demo
**Red Signal Timing 🚦**

![20250505_15h09m36s_grim](https://github.com/user-attachments/assets/26389a15-0dd8-4e4e-8da0-bc4256676ee3)


**Yellow Signal Timing 🚦**

![20250505_15h09m48s_grim](https://github.com/user-attachments/assets/6ca6afe5-49b2-4559-a623-4b3262db1464)


**Green Timing 🚦**

![20250505_15h09m56s_grim](https://github.com/user-attachments/assets/5423df3f-d90e-46f2-95b1-429e62e46952)


## 📁 Project Structure

```bash
├── YOLO_Model/              # Contains YOLO model files and configurations
├── vehicle_detection.py     # Script for detecting and counting vehicles using YOLO
├── signal_controller.py     # Controls traffic signal LEDs based on traffic density
├── requirements.txt         # Python dependencies for the project
└── README.md                # Project documentation
```



## 🚀 Future Enhancements

- Integrate cloud-based traffic analytics dashboard
- Multi-intersection synchronization
- Emergency vehicle prioritization
- Night vision camera support

## 📝 License

This project is for academic use and is open-source for educational and non-commercial purposes.

---

Developed as a Final Year Project in Electronics and Communication Engineering at BVC Engineering College, Odalarevu.
