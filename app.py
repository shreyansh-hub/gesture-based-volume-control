from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import pyautogui
from math import hypot
import numpy as np
import time
import threading

app = Flask(__name__)

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

prev_volume = 0
last_press_time = 0
muted = False
camera_active = True
camera_instance = None
hand_detected = False

# 👉 NEW: Gesture info
gesture_type = "None"
gesture_quality = "N/A"

lock = threading.Lock()

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            raise Exception("Could not open camera")
        print("Camera opened")
        
    def __del__(self):
        if hasattr(self, 'video'):
            self.video.release()
            print("Camera released")
    
    def release(self):
        if self.video.isOpened():
            self.video.release()
            print("Camera released and light turned off")
    
    def get_frame(self):
        global prev_volume, last_press_time, muted, hand_detected
        global gesture_type, gesture_quality
        
        if not self.video.isOpened():
            return None
            
        success, frame = self.video.read()
        if not success:
            return None
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        hand_detected = False
        gesture_type = "None"
        gesture_quality = "N/A"
        
        if results.multi_hand_landmarks:
            hand_detected = True
            
            for hand_landmark in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmark.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                
                if lm_list:
                    x1, y1 = lm_list[4][1], lm_list[4][2]
                    x2, y2 = lm_list[8][1], lm_list[8][2]
                    
                    cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                    cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    
                    length = hypot(x2 - x1, y2 - y1)

                    # 👉 Gesture Type
                    if length > 150:
                        gesture_type = "Volume Up"
                    elif length < 60:
                        gesture_type = "Volume Down"
                    else:
                        gesture_type = "Stable"

                    # 👉 Gesture Quality
                    if length > 120:
                        gesture_quality = "Excellent"
                    elif length > 80:
                        gesture_quality = "Good"
                    else:
                        gesture_quality = "Poor"

                    volume = np.interp(length, [30, 200], [0, 100])
                    volume = int(np.clip(volume, 0, 100))
                    smooth_volume = int(prev_volume + (volume - prev_volume) * 0.25)
                    
                    current_time = time.time()
                    if current_time - last_press_time > 0.15:
                        if smooth_volume > prev_volume:
                            pyautogui.press("volumeup")
                        elif smooth_volume < prev_volume:
                            pyautogui.press("volumedown")
                        last_press_time = current_time
                    prev_volume = smooth_volume
                    
                    fingers_folded = 0
                    tips_ids = [8, 12, 16, 20]
                    for tip in tips_ids:
                        if lm_list[tip][2] > lm_list[tip - 2][2]:
                            fingers_folded += 1
                    
                    if lm_list[4][1] < lm_list[3][1]:
                        fingers_folded += 1
                    
                    if fingers_folded == 5:
                        gesture_type = "Mute"
                        if not muted:
                            pyautogui.press("volumemute")
                            muted = True
                    else:
                        if muted:
                            pyautogui.press("volumemute")
                            muted = False
                    
                    bar_height = np.interp(smooth_volume, [0, 100], [400, 150])
                    cv2.rectangle(frame, (50, 150), (85, 400), (0, 0, 255), 3)
                    cv2.rectangle(frame, (50, int(bar_height)), (85, 400), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, f'Volume: {smooth_volume}%', (40, 450),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                
                mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
        
        # 👉 Display Gesture Info on Camera
        # cv2.putText(frame, f"Gesture: {gesture_type}", (20, 40),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        # cv2.putText(frame, f"Quality: {gesture_quality}", (20, 80),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # if muted:
        #     cv2.putText(frame, "MUTED", (w // 2 - 50, 130),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

def create_black_frame():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    text = "CAMERA STOPPED"
    text2 = "Press 'Start Camera' to resume"
    
    cv2.putText(frame, text, (120, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    cv2.putText(frame, text2, (90, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 1)
    
    ret, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()

def generate_frames():
    global camera_active, camera_instance
    
    while True:
        with lock:
            if camera_active and camera_instance is None:
                try:
                    camera_instance = VideoCamera()
                except Exception as e:
                    print(f"Error opening camera: {e}")
                    time.sleep(1)
                    continue
            
            if not camera_active and camera_instance is not None:
                camera_instance.release()
                camera_instance = None
        
        if camera_active and camera_instance is not None:
            frame = camera_instance.get_frame()
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                time.sleep(0.1)
        else:
            black_frame = create_black_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + black_frame + b'\r\n')
            time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gesture_status', methods=['GET'])
def gesture_status():
    if not camera_active:
        status = 'inactive'
    elif hand_detected:
        status = 'detecting'
    else:
        status = 'ready'
    return jsonify({'status': status})

# 👉 NEW API for gesture info
@app.route('/gesture_info', methods=['GET'])
def gesture_info():
    return jsonify({
        'gesture': gesture_type,
        'quality': gesture_quality
    })

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera_active, camera_instance, hand_detected
    with lock:
        camera_active = False
        hand_detected = False
        if camera_instance is not None:
            camera_instance.release()
            camera_instance = None
    return jsonify({'status': 'stopped'})

@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera_active
    with lock:
        camera_active = True
    return jsonify({'status': 'started'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
