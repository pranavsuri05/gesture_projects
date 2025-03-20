import cv2
import mediapipe as mp
import numpy as np
import os  # To run AppleScript commands

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Mac-friendly media control functions
def control_music(gesture):
    if gesture == "play_pause":
        os.system("osascript -e 'tell application \"System Events\" to key code 49'")  # Spacebar for play/pause
    elif gesture == "next":
        os.system("osascript -e 'tell application \"Music\" to next track'")
    elif gesture == "previous":
        os.system("osascript -e 'tell application \"Music\" to previous track'")
    elif gesture == "volume_up":
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
    elif gesture == "volume_down":
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")

# Gesture detection function
def detect_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # Gesture logic
    if index_tip.y < middle_tip.y < ring_tip.y < pinky_tip.y:
        return "play_pause"  # Index finger up
    elif index_tip.x > thumb_tip.x and index_tip.y < thumb_tip.y:
        return "next"  # Swipe right
    elif index_tip.x < thumb_tip.x and index_tip.y < thumb_tip.y:
        return "previous"  # Swipe left
    elif thumb_tip.y < index_tip.y and thumb_tip.y < pinky_tip.y:
        return "volume_up"  # Thumb up
    elif thumb_tip.y > index_tip.y and thumb_tip.y > pinky_tip.y:
        return "volume_down"  # Thumb down
    return None

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror the image
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    gesture_detected = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture_detected = detect_gesture(hand_landmarks)
    
    # Display command on screen
    if gesture_detected:
        control_music(gesture_detected)
        text = f"Action: {gesture_detected.replace('_', ' ').title()}"
        cv2.putText(frame, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    # Show webcam feed
    cv2.imshow("SignTune - AI Music Controller", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()