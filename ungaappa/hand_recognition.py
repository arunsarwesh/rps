import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def detect_hand_gesture(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Simple logic: Check finger positions
            landmarks = hand_landmarks.landmark
            thumb_tip = landmarks[4].y
            index_tip = landmarks[8].y
            middle_tip = landmarks[12].y

            if thumb_tip > index_tip and middle_tip > index_tip:
                return "rock"
            elif thumb_tip < index_tip and middle_tip < index_tip:
                return "paper"
            else:
                return "scissors"
    
    return None
