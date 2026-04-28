# Gesture Based Volume Control

Control your system volume using hand gestures in real-time using computer vision.

---

## How it works
MediaPipe detects your hand landmarks in real time through the webcam. The app then measures the distance between your thumb tip and index finger tip, maps that distance to a 0–100 volume range, and uses PyAutoGUI to actually change the system volume. Close your fist to mute.
The webcam feed runs through Flask so you can see what the camera sees in a browser tab while it's running.

---

## Features

- Real-time hand tracking using MediaPipe
- Volume control using finger distance
- Mute gesture (closed fist)
- Live webcam streaming
- Interactive UI (Start/Stop camera)

---

## Tech Stack

- Python
- Flask
- OpenCV
- MediaPipe
- PyAutoGUI

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/gesture-volume-control.git
   cd gesture-volume-control
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Project**
   ```bash
   python app.py
   ```

4. **Access the Web UI**
   Open your browser and navigate to: `http://localhost:5000`

---

## How it Works

1. **Detection:** Hand landmarks are detected using the MediaPipe Hands solution.
2. **Calculation:** The system calculates the Euclidean distance between specific landmarks (e.g., thumb tip and index tip).
3. **Mapping:** This distance is mapped to a percentage (0–100) representing the system volume.
4. **Execution:** Python sends keyboard commands or API calls to the operating system to adjust the volume level in real-time.

---

> **Note:** PyAutoGUI behaves differently across operating systems. On **macOS**, you may need to grant accessibility permissions. On **Windows**, it works out of the box.

---

## Future Improvements

- [ ] Screen brightness control integration
- [ ] Support for custom user-defined gestures
- [ ] Mobile-responsive control interface
- [ ] Advanced UI/UX animations for the web dashboard

---
