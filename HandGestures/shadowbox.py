import cv2
import mediapipe as mp
import numpy as np
import time
import random

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils  

# Open webcam
cap = cv2.VideoCapture(0)

# Track hand position, speed, and scoring
prev_x, prev_y = None, None
prev_time = time.time()
score = 0
game_start_time = time.time()
time_limit = 30  
game_over = False  

# AI Opponent Punch Timer
opponent_action_time = time.time()
opponent_dodge_window = 1.5  
dodge_success = False
reaction_feedback = ""
opponent_punch_type = "None"

# Speed tracking
speed_list = []
average_speed = 0

# Feedback Messages
positive_feedback = ["Nice Job! 💥", "Power Punch! ⚡", "Fast Hands! 🏎️", "KO Shot! 🥊"]
negative_feedback = ["Too Slow! 🐢", "Weak Punch! 😴", "Try Again! 🔄"]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Get current time
    curr_time = time.time()
    time_left = max(0, int(time_limit - (curr_time - game_start_time)))  

    if time_left == 0:
        game_over = True

    if results.multi_hand_landmarks and not game_over:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get wrist position
            wrist = hand_landmarks.landmark[0]
            x, y = int(wrist.x * frame.shape[1]), int(wrist.y * frame.shape[0])

            if prev_x is not None and prev_y is not None:
                dx = x - prev_x
                dy = y - prev_y
                movement = np.sqrt(dx**2 + dy**2)  
                time_diff = curr_time - prev_time  

                # **Fix: Only count punches if movement is above threshold**
                punch = None
                if movement > 60 and time_diff > 0.1:  # **Only big movements**
                    if abs(dx) > 40 and abs(dy) < 20:
                        punch = "Jab" if dx > 0 else "Cross"
                    elif abs(dx) < 20 and abs(dy) > 40:
                        punch = "Uppercut"
                    elif abs(dx) > 40 and abs(dy) > 30:
                        punch = "Hook"

                    # **Fix: Only Score When a Punch is Detected**
                    if punch:
                        speed_score = max(10, int(300 / (time_diff + 1)))  
                        score += speed_score  
                        prev_time = curr_time  

                        # AI Feedback
                        reaction_feedback = random.choice(positive_feedback) if speed_score > 15 else random.choice(negative_feedback)

                        # Track Speed
                        speed_list.append(speed_score)
                        if len(speed_list) > 5:
                            speed_list.pop(0)
                        average_speed = sum(speed_list) // len(speed_list)

                        # Display Punch Type
                        cv2.putText(frame, f"{punch}!", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                                    1.2, (0, 255, 0), 3, cv2.LINE_AA)

            prev_x, prev_y = x, y  

    # AI REACTION MODE  
    if not game_over and curr_time - opponent_action_time > random.randint(3, 6):  
        opponent_punch_type = random.choice(["Right Hook", "Straight"])
        dodge_success = False  
        opponent_action_time = curr_time  

    if not game_over and curr_time - opponent_action_time < opponent_dodge_window:
        cv2.rectangle(frame, (50, 150), (600, 230), (0, 0, 255), -1)  
        cv2.putText(frame, f"DODGE {opponent_punch_type}!", (80, 210), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2.3, (255, 255, 255), 6, cv2.LINE_AA)

        if prev_x is not None and abs(prev_x - x) > 50:
            dodge_success = True  

    if dodge_success and not game_over:
        cv2.putText(frame, "Dodged! 🏃‍♂️", (250, 350), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0, 255, 0), 6, cv2.LINE_AA)
        dodge_success = False  

    # Display Score, Timer, & AI Feedback
    if not game_over:
        cv2.putText(frame, f"Score: {score}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1.5, (255, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(frame, f"Time Left: {time_left}s", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                    1.5, (0, 165, 255), 4, cv2.LINE_AA)
        cv2.putText(frame, f"Avg Speed: {average_speed}", (frame.shape[1] - 280, 100),  
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 4, cv2.LINE_AA)  

    if reaction_feedback and not game_over:
        cv2.putText(frame, reaction_feedback, (frame.shape[1] - 450, 350), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 215, 0), 6, cv2.LINE_AA)  

    if game_over:
        cv2.putText(frame, "TIME OVER", (frame.shape[1] // 3, frame.shape[0] // 2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 8, cv2.LINE_AA)
        cv2.putText(frame, f"Final Score: {score}", (frame.shape[1] // 3, frame.shape[0] // 2 + 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 215, 0), 6, cv2.LINE_AA)  

    cv2.imshow("ShadowBox AI", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()