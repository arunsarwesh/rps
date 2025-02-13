import React, { useRef, useState, useEffect } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import rockImg from "../assets/rock.png";
import paperImg from "../assets/paper.jpeg";
import scissorImg from "../assets/scissor.jpeg";

const moves = {
    rock: rockImg,
    paper: paperImg,
    scissors: scissorImg,
};

const WebcamCapture = () => {
    const webcamRef = useRef(null);
    const [gameData, setGameData] = useState(null);
    const [countdown, setCountdown] = useState(2);

    // Function to capture a frame and send it to the backend
    const captureFrame = async () => {
        if (webcamRef.current) {
            const imageSrc = webcamRef.current.getScreenshot(); // Capture frame

            if (imageSrc) {
                try {
                    const response = await axios.post("http://192.168.28.123:8000/recognize/", {
                        image: imageSrc,
                    });

                    setGameData(response.data);
                } catch (error) {
                    console.error("Error sending frame:", error);
                }
            }
        }
    };

    useEffect(() => {
        const interval = setInterval(() => {
            captureFrame();
            setCountdown(2);
        }, 2000);

        const countdownInterval = setInterval(() => {
            setCountdown((prevCountdown) => (prevCountdown > 0 ? prevCountdown - 1 : 2));
        }, 1000);

        return () => {
            clearInterval(interval);
            clearInterval(countdownInterval);
        };
    }, []);

    return (
        <div className="flex flex-col items-center justify-center p-6 bg-gray-100 rounded-lg shadow-lg text-center">
            <h2 className="text-2xl font-bold mb-4">Rock Paper Scissors - Hand Gesture Game</h2>

            {/* Webcam */}
            <Webcam ref={webcamRef} screenshotFormat="image/jpeg" className="rounded-lg w-0 h-0 mx-auto mb-4" />

            {/* Game Interaction UI */}
            {gameData && (
                <div className="flex flex-col items-center mt-4">
                    {/* User Move Display */}
                    <div className="flex gap-4">
                        {Object.keys(moves).map((move) => (
                            <img
                                key={move}
                                src={moves[move]}
                                alt={move}
                                className={`w-20 transition-opacity duration-300 ${
                                    gameData.user_move === move ? "opacity-100 scale-110" : "opacity-40"
                                }`}
                            />
                        ))}
                    </div>
                    <p className="text-lg font-semibold mt-2">👤 Your Move: {gameData.user_move}</p>

                    {/* Computer Move Display */}
                    <div className="flex gap-4 mt-4">
                        {Object.keys(moves).map((move) => (
                            <img
                                key={move}
                                src={moves[move]}
                                alt={move}
                                className={`w-20 transition-opacity duration-300 ${
                                    gameData.computer_move === move ? "opacity-100 scale-110" : "opacity-40"
                                }`}
                            />
                        ))}
                    </div>
                    <p className="text-lg font-semibold mt-2">🤖 Computer Move: {gameData.computer_move}</p>

                    {/* Scores & Result */}
                    <div className="p-4 bg-white rounded-lg shadow-md mt-6 w-80">
                        <h3 className="text-lg font-bold mb-2">Game Result</h3>
                        <p><strong>Winner:</strong> {gameData.winner}</p>
                        <p>👤 <strong>User Score:</strong> {gameData.user_score}</p>
                        <p>🤖 <strong>Computer Score:</strong> {gameData.computer_score}</p>
                        <p className="text-sm text-gray-600 mt-2">Next capture in: {countdown} seconds</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default WebcamCapture;
