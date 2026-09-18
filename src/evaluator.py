import csv
import os
import time

class Evaluator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.filename = os.path.join(self.output_dir, f"session_{int(time.time())}.csv")
        self.data = []

    def log_frame(self, fps, latency, ear, mar):
        self.data.append([time.time(), fps, latency, ear, mar])

    def export(self):
        with open(self.filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "fps", "latency_ms", "ear", "mar"])
            writer.writerows(self.data)