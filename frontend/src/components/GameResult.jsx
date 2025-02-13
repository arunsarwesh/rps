import { useEffect, useState } from "react";
import axios from "axios";

const GameResult = () => {
    const [gameData, setGameData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get("http://192.168.28.123:8000/recognize/");
                setGameData(response.data);
            } catch (err) {
                setError("Failed to fetch data");
            }
        };

        fetchData();
    }, []);

    if (error) return <p className="text-red-500">{error}</p>;
    if (!gameData) return <p>Loading...</p>;

    return (
        <div className="p-5 bg-gray-100 rounded-lg shadow-md w-80 mx-auto mt-10">
            <h2 className="text-xl font-bold mb-2 text-center">Game Result</h2>
            <p><strong>User Move:</strong> {gameData.user_move}</p>
            <p><strong>Computer Move:</strong> {gameData.computer_move}</p>
            <p><strong>Winner:</strong> {gameData.winner}</p>
            <p><strong>User Score:</strong> {gameData.user_score}</p>
            <p><strong>Computer Score:</strong> {gameData.computer_score}</p>
        </div>
    );
};

export default GameResult;
