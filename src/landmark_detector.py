import cv2
import mediapipe as mp
import numpy as np

class LandmarkDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.MOUTH = [61, 81, 13, 311, 291, 402, 14, 178]

    def extract_landmarks(self, frame_rgb):
        results = self.face_mesh.process(frame_rgb)
        if not results.multi_face_landmarks:
            return None, None, None
        landmarks = results.multi_face_landmarks[0].landmark
        h, w, _ = frame_rgb.shape
        coords = np.array([(int(l.x * w), int(l.y * h)) for l in landmarks])
        return coords[self.LEFT_EYE], coords[self.RIGHT_EYE], coords[self.MOUTH]