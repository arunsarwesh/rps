import cv2
import numpy as np
import base64
import mediapipe as mp
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import GameScore

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)

def get_user_move(hand_landmarks):
    # Check if fingers are extended.
    # For each finger, compare the tip and the pip (proximal interphalangeal) joint.
    index_extended = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_extended = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    ring_extended = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
    pinky_extended = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y

    # Count the number of extended fingers.
    extended_count = sum([index_extended, middle_extended, ring_extended, pinky_extended])

    # If no fingers are extended, then it's rock.
    if extended_count == 0:
        return "rock"
    
    # If exactly index and middle are extended, then it's scissors.
    if extended_count == 2 and index_extended and middle_extended:
        return "scissors"
    
    # Otherwise, it's paper.
    return "paper"

class HandGestureRecognitionView(APIView):
    def post(self, request):
        image_data = request.data.get("image")
        if not image_data:
            return JsonResponse({"error": "No image provided"}, status=400)

        # Convert base64 image to OpenCV format.
        if "," in image_data:
            encoded_data = image_data.split(",")[1]  # Remove the header
        else:
            encoded_data = image_data
        try:
            decoded_data = base64.b64decode(encoded_data)
        except Exception as e:
            return JsonResponse({"error": "Invalid image data"}, status=400)
        nparr = np.frombuffer(decoded_data, np.uint8)
        if nparr.size == 0:
            return JsonResponse({"error": "Image data is empty after base64 decode"}, status=400)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return JsonResponse({"error": "Image data could not be decoded"}, status=400)

        # Convert to RGB for MediaPipe processing.
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Use the new helper function to determine the user's move.
                user_move = get_user_move(hand_landmarks)

                # Simulate computer move.
                computer_move = np.random.choice(["rock", "paper", "scissors"])

                # Determine winner.
                if user_move == computer_move:
                    result = "tie"
                elif (user_move == "rock" and computer_move == "scissors") or \
                     (user_move == "scissors" and computer_move == "paper") or \
                     (user_move == "paper" and computer_move == "rock"):
                    result = "user"
                else:
                    result = "computer"

                # Update scores.
                score = GameScore.objects.last() or GameScore.objects.create()
                if result == "user":
                    score.user_score += 1
                elif result == "computer":
                    score.computer_score += 1
                score.save()

                return JsonResponse({
                    "user_move": user_move,
                    "computer_move": computer_move,
                    "winner": result,
                    "user_score": score.user_score,
                    "computer_score": score.computer_score
                })

        return JsonResponse({"user_move": "No hand detected"}, status=200)