import argparse
import cv2
import time
from src.camera_stream import CameraStream
from src.landmark_detector import LandmarkDetector
from src.metrics_calculator import MetricsCalculator
from src.temporal_analyzer import TemporalAnalyzer
from src.evaluator import Evaluator
from src.alert_system import AlertSystem

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=int, default=0)
    parser.add_argument("--ear-thresh", type=float, default=0.20)
    parser.add_argument("--consec-frames", type=int, default=16)
    parser.add_argument("--output-dir", type=str, default="outputs")
    parser.add_argument("--no-display", action="store_true")
    args = parser.parse_args()

    stream = CameraStream(source=args.source)
    detector = LandmarkDetector()
    analyzer = TemporalAnalyzer(args.ear_thresh, args.consec_frames)
    evaluator = Evaluator(args.output_dir)
    alert_system = AlertSystem()

    prev_time = time.time()
    occlusion_counter = 0

    while True:
        start_time = time.time()
        frames = stream.get_frame()
        
        if frames is None or frames[0] is None or frames[1] is None:
            time.sleep(0.01)
            continue
        
        original_frame, processed_frame = frames
        rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

        left_eye, right_eye, mouth = detector.extract_landmarks(rgb_frame)

        ear = 0.0
        mar = 0.0
        blinks = analyzer.blink_count
        alert = analyzer.drowsy_alert

        if left_eye is not None and right_eye is not None and mouth is not None:
            occlusion_counter = 0
            
            ear_left = MetricsCalculator.calculate_ear(left_eye)
            ear_right = MetricsCalculator.calculate_ear(right_eye)
            ear = (ear_left + ear_right) / 2.0
            mar = MetricsCalculator.calculate_mar(mouth)
            
            blinks, alert = analyzer.update(ear)
            
            for pt in left_eye:
                cv2.circle(original_frame, tuple(pt), 2, (0, 255, 0), -1)
            for pt in right_eye:
                cv2.circle(original_frame, tuple(pt), 2, (0, 255, 0), -1)
            for pt in mouth:
                cv2.circle(original_frame, tuple(pt), 2, (0, 0, 255), -1)
        else:
            occlusion_counter += 1
            if occlusion_counter >= args.consec_frames:
                alert = True
                cv2.putText(original_frame, "WARNING: FACE NOT VISIBLE!", (10, 200), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

        if alert:
            alert_system.trigger_alarm()
            if occlusion_counter < args.consec_frames:
                cv2.putText(original_frame, "DROWSINESS ALERT!", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        curr_time = time.time()
        time_diff = curr_time - prev_time
        fps = 1.0 / time_diff if time_diff > 0 else 0.0
        prev_time = curr_time
        latency = (time.time() - start_time) * 1000

        evaluator.log_frame(fps, latency, ear, mar)

        cv2.putText(original_frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(original_frame, f"MAR: {mar:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(original_frame, f"Blinks: {blinks}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(original_frame, f"FPS: {fps:.1f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if not args.no_display:
            try:
                cv2.imshow("Monitor", original_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except cv2.error:
                pass
        else:
            time.sleep(0.01)

    stream.release()
    try:
        cv2.destroyAllWindows()
    except cv2.error:
        pass
    evaluator.export()

if __name__ == "__main__":
    main()