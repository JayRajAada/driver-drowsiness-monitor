class TemporalAnalyzer:
    def __init__(self, ear_thresh, consec_frames):
        self.ear_thresh = ear_thresh
        self.consec_frames = consec_frames
        self.counter = 0
        self.blink_count = 0
        self.drowsy_alert = False

    def update(self, ear):
        if ear < self.ear_thresh:
            self.counter += 1
            if self.counter >= self.consec_frames:
                self.drowsy_alert = True
        else:
            if 1 <= self.counter < self.consec_frames:
                self.blink_count += 1
            self.counter = 0
            self.drowsy_alert = False
        return self.blink_count, self.drowsy_alert