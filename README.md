# 🐍 Voice-Controlled Snake Game

A classic snake game with a modern twist - control the snake using your voice! Built with Python, Pygame, and Google Speech Recognition.

## 🎮 Features

- **Voice Control**: Navigate the snake using Turkish voice commands
  - "Yukarı" (Up)
  - "Aşağı" (Down)
  - "Sol" (Left)
  - "Sağ" (Right)
- **Classic Gameplay**: Eat food to grow, avoid hitting yourself
- **Screen Wrapping**: Snake wraps around when reaching screen edges
- **Real-time Speech Recognition**: Continuous voice command listening using Google Speech API

## 🛠️ Technologies

- **Python 3**
- **Pygame** - Game rendering and display
- **SpeechRecognition** - Voice command processing
- **Google Speech API** - Turkish speech-to-text conversion

## 📋 Requirements

```bash
pip install pygame
pip install SpeechRecognition
pip install PyAudio
```

> **Note**: PyAudio is required for microphone access. On Windows, you may need to install it using:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

## 🚀 Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Emre-Kahveci/voice-controlled-snake-game.git
   cd voice-controlled-snake-game
   ```

2. Install dependencies:
   ```bash
   pip install pygame SpeechRecognition PyAudio
   ```

3. Run the game:
   ```bash
   python snake_game.py
   ```

4. Wait for microphone calibration (keep silent during this phase)

5. Use voice commands to control the snake:
   - Say **"Yukarı"** to go up
   - Say **"Aşağı"** to go down
   - Say **"Sol"** to go left
   - Say **"Sağ"** to go right

## ⚙️ Configuration

You can modify game settings in `snake_game.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `WIDTH` | 800 | Game window width |
| `HEIGHT` | 600 | Game window height |
| `SNAKE_SIZE` | 3 | Initial snake length |
| `SNAKE_BLOCK_SIZE` | 20 | Size of each snake segment |
| `GAME_SPEED` | 3 | Game speed (frames per second) |

To change the microphone device, modify `device_index` in `speech_to_text.py`.

## 📁 Project Structure

```
voice-controlled-snake-game/
├── snake_game.py       # Main game logic and rendering
├── speech_to_text.py   # Voice recognition module
├── snake game.ipynb    # Jupyter notebook version
├── .gitignore
└── README.md
```

## 🎯 How It Works

1. **Game Loop**: The main game runs in a continuous loop, handling movement, collision detection, and rendering
2. **Voice Thread**: A separate thread continuously listens for voice commands using the microphone
3. **Speech Processing**: Voice input is converted to text using Google's Speech Recognition API (Turkish language)
4. **Direction Mapping**: Recognized commands are mapped to snake movement directions

## 📝 License

This project is open source and available for educational purposes.

## 👤 Author

**Emre Kahveci**

---

*Enjoy the game and have fun controlling the snake with your voice!* 🎤🐍
