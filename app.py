# app.py (Add clear history endpoint)
from flask import Flask, render_template, Response, request, jsonify
import cv2
import mediapipe as mp
import pyautogui
import time
import math
import numpy as np
import screen_brightness_control as sbc
import threading
from collections import Counter

app = Flask(__name__)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2)

prev_gesture = None
current_gesture = "None"
gesture_history = []
mute_triggered = False
streaming = False
output_frame = None
lock = threading.Lock()

# Gesture detection function
def detect_gesture(lst):
    thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2
    fingers = []

    if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
        fingers.append(1)
    else:
        fingers.append(0)

    fingers.append(1 if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh else 0)
    fingers.append(1 if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh else 0)
    fingers.append(1 if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh else 0)
    fingers.append(1 if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh else 0)

    if fingers == [1, 1, 1, 1, 1]:
        return "Palm"
    elif fingers == [0, 0, 0, 0, 0]:
        return "Fist"
    elif fingers == [0, 1, 0, 0, 0]:
        return "Index Left" if lst.landmark[8].x * 100 < lst.landmark[7].x * 100 else "Index Right"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Two Fingers Left" if lst.landmark[8].x * 100 < lst.landmark[7].x * 100 else "Two Fingers Right"

    thumb_tip = lst.landmark[4]
    index_tip = lst.landmark[8]
    distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)

    if distance < 0.05:
        return "Pinch"

    return "None"

# Camera Thread
cap = None

def camera_stream():
    global cap, output_frame, streaming, prev_gesture, mute_triggered, current_gesture, gesture_history
    cap = cv2.VideoCapture(0)

    while streaming:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        gestures = []
        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[idx].classification[0].label
                gesture = detect_gesture(hand_landmarks)
                gestures.append((gesture, hand_label))

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if gestures:
                current_gesture = gestures[0][0]
                if current_gesture != "None":
                    if not gesture_history or gesture_history[-1] != current_gesture:
                        gesture_history.append(current_gesture)

            if len(gestures) == 2 and all(g[0] == "Fist" for g in gestures):
                if not mute_triggered:
                    pyautogui.press("volumemute")
                    mute_triggered = True
            else:
                mute_triggered = False

            for gesture, hand_label in gestures:
                if gesture == "Two Fingers Right":
                    sbc.set_brightness(min(sbc.get_brightness()[0] + 10, 100))
                    time.sleep(0.5)
                elif gesture == "Two Fingers Left":
                    sbc.set_brightness(max(sbc.get_brightness()[0] - 10, 0))
                    time.sleep(0.5)
                elif gesture != prev_gesture:
                    if gesture == "Palm":
                        pyautogui.press("space")
                    elif gesture == "Index Right":
                        pyautogui.press("right")
                    elif gesture == "Index Left":
                        pyautogui.press("left")
                    elif gesture == "Pinch":
                        if hand_label == "Right":
                            pyautogui.press("volumeup")
                        else:
                            pyautogui.press("volumedown")
                    prev_gesture = gesture
        else:
            current_gesture = "None"

        ret, buffer = cv2.imencode('.jpg', frame)
        with lock:
            output_frame = buffer.tobytes()

    cap.release()


def gen_frames():
    global output_frame
    while streaming:
        with lock:
            if output_frame is None:
                continue
            frame = output_frame

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_stream', methods=['POST'])
def start_stream():
    global streaming
    if not streaming:
        streaming = True
        threading.Thread(target=camera_stream).start()
    return jsonify(status="started")

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global streaming
    streaming = False
    return jsonify(status="stopped")

@app.route('/clear_history', methods=['POST'])
def clear_history():
    global gesture_history
    gesture_history.clear()
    return jsonify(status="cleared")

@app.route('/get_gesture_status')
def get_gesture_status():
    counts = dict(Counter(gesture_history))
    return jsonify(gesture=current_gesture, history=gesture_history, counts=counts)

if __name__ == '__main__':
    app.run(debug=True)

# index.html (Add Clear History button and JS logic)

