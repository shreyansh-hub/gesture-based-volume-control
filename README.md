# 🎛 Gesture Based Volume Control

Control your system volume using hand gestures in real-time using computer vision.

---

## 🚀 Features
- Real-time hand tracking using MediaPipe
- Volume control using finger distance
- Mute gesture (closed fist)
- Live webcam streaming
- Interactive UI (Start/Stop camera)

---

## 🛠 Tech Stack
- Python
- Flask
- OpenCV
- MediaPipe
- PyAutoGUI

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/your-username/gesture-volume-control.git](https://github.com/your-username/gesture-volume-control.git)
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

## 🧠 How it Works
1. **Detection:** Hand landmarks are detected using the MediaPipe Hands solution.
2. **Calculation:** The system calculates the Euclidean distance between specific landmarks (e.g., thumb tip and index tip).
3. **Mapping:** This distance is mapped to a percentage (0-100) representing the system volume.
4. **Execution:** Python sends keyboard commands or API calls to the operating system to adjust the volume level in real-time.

---

## 🚀 Future Improvements
- [ ] Screen brightness control integration.
- [ ] Support for custom user-defined gestures.
- [ ] Mobile-responsive control interface.
- [ ] Advanced UI/UX animations for the web dashboard.

---

## 👨‍💻 Author
**Shreyansh Mishra**

---

* **Requirements File:** Ensure your `requirements.txt` includes specific versions for `mediapipe`, `opencv-python`, and `Flask` to avoid compatibility issues for other users.
* **Cross-Platform Note:** Since you are using `PyAutoGUI` for volume, mention in a "Note" section if it works differently on macOS vs. Windows (as macOS often requires accessibility permissions).
* **Screenshot:** If you don't have a `demo.png` yet, a GIF showing the volume bar moving while you pinch your fingers is usually very effective for GitHub projects.
