# SignTune & ShadowBox

## SignTune - AI-Powered Music Controller
SignTune is an AI-driven music controller that enables stage performers and users to control music using hand gestures. By leveraging OpenCV and MediaPipe for hand tracking, SignTune translates hand movements into commands for playing, pausing, skipping tracks, and adjusting volume levels.

### Features:
- **Gesture-based music control**: Play/Pause, Next, Previous, Volume Up, Volume Down.
- **Real-time hand tracking** using OpenCV and MediaPipe.
- **MacOS integration** via AppleScript to control system music playback.

### How It Works:
1. Tracks hand movements using a webcam.
2. Detects predefined gestures.
3. Sends corresponding commands to control media playback.

---

## ShadowBox - AI-Powered Virtual Boxing Trainer
ShadowBox is an interactive AI boxing trainer that enhances your reflexes, speed, and power by tracking punches and dodging actions. It provides real-time feedback and AI opponent reactions for an engaging workout.

### Features:
- **Real-time punch detection**: Recognizes jabs, hooks, crosses, and uppercuts.
- **Speed tracking & scoring**: Measures punch speed and accuracy to provide scores.
- **AI opponent simulation**: Reacts with punches, requiring users to dodge.
- **Live feedback system**: Encourages with positive reinforcement or constructive feedback.

### How It Works:
1. Tracks hand and wrist movements using OpenCV and MediaPipe.
2. Detects different punch types and assigns scores based on speed and accuracy.
3. Introduces an AI opponent that throws virtual punches requiring dodging.
4. Displays scores, reaction feedback, and remaining time.

---

## Installation & Requirements
### Prerequisites:
- Python 3.x
- OpenCV
- MediaPipe
- NumPy

### Installation:
```sh
pip install opencv-python mediapipe numpy
```

### Running the Applications:
For **SignTune**:
```sh
python signtune.py
```

For **ShadowBox**:
```sh
python shadowbox.py
```

---

## Controls & Gestures
### SignTune Gesture Mapping:
| Gesture       | Action        |
|--------------|--------------|
| Index up     | Play/Pause   |
| Swipe right  | Next Track   |
| Swipe left   | Previous Track |
| Thumb up     | Volume Up    |
| Thumb down   | Volume Down  |

### ShadowBox Punch Detection:
| Punch Type  | Detection Criteria |
|------------|--------------------|
| Jab       | Quick horizontal motion |
| Cross     | Strong horizontal punch |
| Hook      | Circular horizontal motion |
| Uppercut  | Vertical punch upwards |

---

## Future Enhancements
- Expanding gesture vocabulary for **SignTune** to include more controls.
- Enhancing AI opponent difficulty in **ShadowBox** with adaptive reactions.
- Introducing a leaderboard system for score tracking.

---

Developed by Pranav Suri 🚀

