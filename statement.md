# Problem Statement & Project Scope

## Problem Statement
Driver fatigue and micro-sleep episodes are major contributors to critical road accidents globally. Existing commercial monitoring solutions often require specialized hardware sensors or high-compute embedded devices. This project provides a real-time, software-based facial landmark monitoring pipeline that calculates spatial geometry metrics from standard camera feeds to detect driver drowsiness and trigger immediate alerts.

## Target Users
* Long-haul drivers operating under fatigue-prone conditions.
* Fleet management operators requiring automated safety monitoring.
* Automotive safety engineers evaluating computer vision fatigue-detection software.

## Project Scope
The system ingests live video streams, applies low-light contrast enhancement (CLAHE), extracts 68 facial landmark coordinates via MediaPipe, and continuously evaluates the Eye Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR). The pipeline tracks frame-by-frame temporal metrics to count eye blinks, detect prolonged eye closures, identify facial occlusion, and record spatial metrics to CSV for analysis.

## Core Requirements

### Functional Requirements
1. **Real-Time Landmark Detection & Preprocessing:** Stream incoming frames, convert to grayscale, apply CLAHE histogram equalization, and extract key eye/mouth landmark coordinates.
2. **Spatial Metric Calculation:** Calculate spatial Euclidean distance ratios (Eye Aspect Ratio - EAR, Mouth Aspect Ratio - MAR) per frame.
3. **Temporal Analysis & Alarm System:** Maintain a consecutive frame threshold state machine to distinguish normal eye blinks from drowsiness, triggering multi-threaded audio alerts upon threshold breach.

### Non-Functional Requirements
1. **Performance & Low Latency:** Maintain frame processing latency below 50ms to sustain real-time performance (>20 FPS).
2. **Portability & Headless Execution:** Execute cross-platform across Windows and Linux environments via command-line interface (CLI) with headless `--no-display` support.
3. **Reliability under Low Lighting:** Adapt to indoor or low-light cabin environments via CLAHE contrast adjustment.
4. **Maintainability & Resource Efficiency:** Modular design separating ingestion, detection, calculation, and evaluation components with CPU usage under 15%.