# EyeTrack-SpaceShooter

Welcome to the EyeTrack-SpaceShooter repository! This project features an innovative space shooting game that utilizes eye-tracking technology to aim and shoot enemies, providing an immersive and hands-free gaming experience.

## Features

- **Eye-Tracking Controls:** Utilize your eye movements to aim and shoot at enemies.
- **Advanced Technologies:** Built using powerful libraries such as OpenCV, MediaPipe, and PyAutoGUI.
- **Engaging Gameplay:** Fast-paced space shooting action that responds to your gaze.
- **Python Implementation:** Entirely developed in Python for easy modification and enhancement.
- **Modular Codebase:** Clean and well-organized code, making it easy for developers to understand and contribute.

## Technologies Used

- **OpenCV:** For real-time computer vision and image processing.
- **MediaPipe:** For robust and efficient eye-tracking.
- **PyAutoGUI:** For simulating mouse and keyboard actions based on eye movements.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- Basic knowledge of Python and computer vision.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/EyeTrack-SpaceShooter.git
   ```
2. Navigate to the project directory:
   ```bash
   cd EyeTrack-SpaceShooter
   ```
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

Run the following command to start the game:
```bash
python space_shooter.py
```

Follow the on-screen instructions to calibrate the eye-tracking system and start playing.

## How It Works

### Eye-Tracking

The game uses MediaPipe to track eye movements in real-time. OpenCV captures the video feed from the webcam, and MediaPipe processes this feed to determine the direction of the player's gaze.

### Aiming and Shooting

PyAutoGUI translates the gaze direction into corresponding mouse movements and clicks, allowing the player to aim and shoot at enemies based on where they look on the screen.

### Game Mechanics

Enemies appear on the screen, and the player must aim using their eyes to shoot them down. The game features various levels of difficulty, increasing the challenge as the player progresses.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to enhance the game, fix bugs, or improve documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Experience a new dimension of gaming with EyeTrack-SpaceShooter! If you have any questions or need further assistance, please open an issue or contact me at your-email@example.com.

---

### Acknowledgments

- Thanks to the developers of OpenCV, MediaPipe, and PyAutoGUI for their amazing libraries.
- Inspired by the endless possibilities of eye-tracking technology.

---

Enjoy the game, and may your gaze be ever accurate!
