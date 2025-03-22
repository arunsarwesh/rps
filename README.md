# Rock-Paper-Scissors Hand Gesture Recognition API

## Overview
This project is a Django REST Framework (DRF) API that enables users to play Rock-Paper-Scissors using hand gestures. The API utilizes OpenCV and MediaPipe to detect hand gestures from an image, determine the user's move, and compare it against a randomly selected move from the computer. The results, including scores, are stored in a Django database.

## Features
- Detects hand gestures (rock, paper, scissors) from an image.
- Compares user and computer moves to determine the winner.
- Stores game scores in a Django model (`GameScore`).
- Provides a RESTful API for image-based gesture recognition.
- Handles errors for invalid or missing images.

## Tech Stack
- **Backend:** Django, Django REST Framework (DRF)
- **Machine Learning:** OpenCV, MediaPipe
- **Database:** SQLite (can be changed to PostgreSQL or MySQL)
- **Frontend (Optional):** Any frontend framework (React, Angular, etc.) that can send images to the API

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Django
- Django REST Framework
- OpenCV (`cv2`)
- MediaPipe
- Pillow
- NumPy

### Clone the Repository
```sh
git clone https://github.com/arunsarwesh/rps.git
cd rock-paper-scissors-api
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Apply Migrations
```sh
python manage.py migrate
```

### Run the Server
```sh
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

## API Endpoints
### Hand Gesture Recognition API
#### Endpoint: `POST /recognize/`
- **Description:** Accepts a base64-encoded image, processes it to detect a hand gesture, and determines the result of the game.
- **Request Body:**
```json
{
    "image": "data:image/png;base64,iVBORw0KGg..."
}
```
- **Response:**
```json
{
    "user_move": "rock",
    "computer_move": "paper",
    "winner": "computer",
    "user_score": 1,
    "computer_score": 2
}
```
- **Error Responses:**
  - `400 Bad Request`: Invalid or missing image data.
  - `200 OK`: No hand detected in the image.

## Project Structure
```
rock-paper-scissors-api/
│── api/
│   ├── migrations/
│   ├── models.py    # Database models
│   ├── views.py     # API logic
│   ├── urls.py      # API routes
│   ├── serializers.py # DRF serializers
│── settings.py      # Django settings
│── manage.py        # Django entry point
│── requirements.txt # Dependencies
│── README.md        # Project documentation
```

## How It Works
1. A user uploads an image containing a hand gesture.
2. The API decodes the image and processes it using OpenCV and MediaPipe.
3. The system classifies the gesture as 'rock', 'paper', or 'scissors'.
4. The API randomly selects a move for the computer.
5. The winner is determined, and scores are updated in the database.
6. The response is sent back to the user.

## Troubleshooting
### Common Issues and Fixes
1. **"Encoded data is missing or too short" error**
   - Ensure the client sends the base64 image correctly without extra characters.
   - Remove the `data:image/png;base64,` header before decoding.

2. **"Invalid image data" error**
   - The image might be corrupted or incorrectly encoded.
   - Try decoding the image manually to verify its validity.

## Future Improvements
- Deploy to a cloud server (AWS, Heroku, or DigitalOcean).
- Implement real-time gesture recognition using WebRTC.
- Develop a frontend interface for better user interaction.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Contact
For any issues or contributions, feel free to reach out:
- **GitHub:** [github.com/yarunsarwesh](https://github.com/arunsarwesh)
- **Email:** sarweshwardeivasihamani@gmail.com

