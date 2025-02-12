import cv2
import numpy as np
import base64
import mediapipe as mp
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import GameScore

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)

class HandGestureRecognitionView(APIView):
    def post(self, request):
        image_data = request.data.get("image")

        if not image_data:
            return JsonResponse({"error": "No image provided"}, status=400)

        # Convert base64 image to OpenCV format
        encoded_data = image_data.split(",")[1]  # Remove the header
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert to RGB for MediaPipe processing
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[4].y
                index_tip = hand_landmarks.landmark[8].y
                middle_tip = hand_landmarks.landmark[12].y

                if thumb_tip > index_tip and middle_tip > index_tip:
                    user_move = "scissor"
                elif thumb_tip < index_tip and middle_tip < index_tip:
                    user_move = "rock"
                else:
                    user_move = "paper"

                # Simulate Computer Move
                computer_move = np.random.choice(["rock", "paper", "scissors"])

                # Determine Winner
                if user_move == computer_move:
                    result = "tie"
                elif (user_move == "rock" and computer_move == "scissors") or \
                     (user_move == "scissors" and computer_move == "paper") or \
                     (user_move == "paper" and computer_move == "rock"):
                    result = "user"
                else:
                    result = "computer"

                # Update Scores
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

        return JsonResponse({"error": "No hand detected"}, status=400)