import cv2

class CameraStream:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        enhanced = self.clahe.apply(gray)
        enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
        return frame, enhanced_bgr

    def release(self):
        self.cap.release()