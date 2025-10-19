# Vision-Controlled Mouse

A Python application that uses computer vision and hand tracking to control your mouse cursor with hand gestures.

## Features

- **Hand Tracking**: Uses MediaPipe to detect and track hand landmarks in real-time
- **Mouse Control**: Move your mouse cursor by moving your index finger
- **Click Gesture**: Click by bringing your thumb and index finger close together
- **Real-time Display**: Shows camera feed with hand landmarks overlaid

## Requirements

- Python 3.7+
- Webcam
- macOS (for PyAutoGUI compatibility)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sakets-dev/vision_controlled_mouse.git
   cd vision_controlled_mouse
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Position your hand in front of the camera
3. Move your index finger to control the mouse cursor
4. Bring your thumb and index finger close together to click
5. Press 'q' to quit the application

## Dependencies

- `opencv-python`: Computer vision library
- `mediapipe`: Hand tracking and pose estimation
- `pyautogui`: Mouse control automation
- `numpy`: Numerical computing

## Camera Permissions

On macOS, you may need to grant camera permissions:
1. Go to System Preferences → Security & Privacy → Camera
2. Allow your terminal application to access the camera
3. Or run: `tccutil reset Camera` in terminal

## How It Works

1. **Camera Capture**: Uses OpenCV to capture video from your webcam
2. **Hand Detection**: MediaPipe processes the video to detect hand landmarks
3. **Landmark Processing**: Extracts finger positions and calculates distances
4. **Mouse Control**: PyAutoGUI moves the mouse cursor based on finger position
5. **Click Detection**: Monitors distance between thumb and index finger for clicks

## Troubleshooting

- **Camera not working**: Ensure camera permissions are granted and no other apps are using the camera
- **Module not found errors**: Make sure all dependencies are installed correctly
- **Poor tracking**: Ensure good lighting and keep your hand visible in the camera frame

## License

This project is open source and available under the MIT License.
