import cv2
import mediapipe as mp
import pyautogui
import time
import math
import numpy as np

# Function to detect gestures, including pinch gestures for volume control
def detect_gesture(lst, hand_label):
    # Track how many fingers are extended
    thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2
    fingers = []

    # Thumb
    if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
        fingers.append(1)  # Thumb is up
    else:
        fingers.append(0)

    # Other four fingers
    fingers.append(1 if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh else 0)
    fingers.append(1 if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh else 0)
    fingers.append(1 if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh else 0)
    fingers.append(1 if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh else 0)

    # Gesture detection logic
    if fingers == [1, 1, 1, 1, 1]:  # All fingers extended (palm)
        return "palm"
    elif fingers == [0, 0, 0, 0, 0]:  # Fist (no fingers extended)
        return "fist"
    elif fingers == [0, 1, 0, 0, 0]:  # Index finger only (facing right or left)
        if lst.landmark[8].x * 100 < lst.landmark[7].x * 100:
            return "index_left"
        else:
            return "index_right"

    # Pinch gesture detection (thumb and index finger close)
    thumb_tip = lst.landmark[4]
    index_tip = lst.landmark[8]
    distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)

    # Threshold to detect pinch (you may need to adjust this)
    pinch_threshold = 0.05
    if distance < pinch_threshold:
        if hand_label == "Right":
            return "pinch_right"
        elif hand_label == "Left":
            return "pinch_left"

    return "none"  # No recognizable gesture


# Initialize camera and Mediapipe
cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=2)  # Detect up to 2 hands

prev_gesture = None

# Main loop to read frames and process gestures
while True:
    ret, frm = cap.read()
    if not ret:
        print("Failed to capture image")
        continue

    frm = cv2.flip(frm, 1)  # Mirror the frame for easier interaction

    # Ensure the frame is in the correct format
    frm_rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
    frm_rgb = np.ascontiguousarray(frm_rgb)

    res = hand_obj.process(frm_rgb)  # Process frame with Mediapipe

    if res.multi_hand_landmarks and res.multi_handedness:
        for idx, hand_keyPoints in enumerate(res.multi_hand_landmarks):
            hand_label = res.multi_handedness[idx].classification[0].label  # 'Left' or 'Right'
            gesture = detect_gesture(hand_keyPoints, hand_label)

            if gesture != prev_gesture:
                # Map gestures to actions
                if gesture == "palm":
                    pyautogui.press("space")  # Play/pause
                elif gesture == "fist":
                    pyautogui.press("volumemute")  # Mute
                elif gesture == "index_right":
                    pyautogui.press("right")  # Skip forward
                elif gesture == "index_left":
                    pyautogui.press("left")  # Rewind
                elif gesture == "pinch_right":
                    pyautogui.press("volumeup")  # Volume up with right hand pinch
                elif gesture == "pinch_left":
                    pyautogui.press("volumedown")  # Volume down with left hand pinch

                prev_gesture = gesture  # Update previous gesture

            # Draw hand landmarks
            drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow("Gesture Control", frm)

    # Exit on ESC key
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
