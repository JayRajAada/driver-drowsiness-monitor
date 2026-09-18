# Real-Time Driver Drowsiness & Eye-Blink Monitor

A computer vision-based system designed to detect driver fatigue in real-time. By extracting facial landmarks and computing spatial geometry metrics (Eye Aspect Ratio and Mouth Aspect Ratio), the system accurately monitors blinks and triggers cross-platform alerts upon detecting prolonged eye closure.

## Features
* **Facial Landmark Extraction:** Utilizes MediaPipe Face Mesh for robust 68-point spatial tracking.
* **Low-Light Enhancement:** Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to maintain accuracy in varying cabin lighting conditions.
* **Temporal State Machine:** Differentiates between normal rapid blinks and sustained drowsiness closures.
* **Cross-Platform Audio Alerts:** Multi-threaded alarm system with graceful OS-specific fallbacks.
* **Headless Execution Support:** CLI-driven architecture with a `--no-display` mode for automated CI/CD evaluation environments.
* **Session Analytics Logging:** Automatically exports detailed performance metrics (FPS, Latency, EAR, MAR) to a timestamped CSV upon completion.

## Repository Structure
```text
├── README.md                 # Setup and execution guide
├── statement.md              # Problem statement and scope definition
├── requirements.txt          # Python dependencies
├── main.py                   # Command-line entry point
├── src/
│   ├── alert_system.py       # Cross-platform audio trigger
│   ├── camera_stream.py      # Video ingestion and CLAHE enhancement
│   ├── evaluator.py          # Session logging to CSV
│   ├── landmark_detector.py  # MediaPipe facial mesh tracking
│   ├── metrics_calculator.py # EAR and MAR geometric computations
│   └── temporal_analyzer.py  # Blink counting and alert threshold logic
└── outputs/                  # Auto-generated directory for CSV logs
```

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/){github-username}/{repo-name}.git
   cd {repo-name}
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux / macOS
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Execution Instructions

The project is fully executable via the command line. To launch with default parameters:
```bash
python main.py
```

To specify custom thresholds and execute without the GUI (headless mode):
```bash
python main.py --source 0 --ear-thresh 0.22 --consec-frames 20 --no-display
```

### Command-Line Arguments

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--source` | `int` / `str` | `0` | Video source index (webcam) or file path. |
| `--ear-thresh` | `float` | `0.20` | Eye Aspect Ratio threshold for detecting eye closure. |
| `--consec-frames` | `int` | `16` | Consecutive frames below EAR threshold to trigger the drowsiness alarm. |
| `--output-dir` | `str` | `"outputs"` | Directory where CSV session metric logs will be saved. |
| `--no-display` | `flag` | `False` | Disables the OpenCV output window for headless environments. |

## User Controls
* Ensure the video window is in focus and press **`q`** to safely terminate the stream and export the session CSV log.