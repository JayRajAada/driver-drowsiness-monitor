from scipy.spatial import distance

class MetricsCalculator:
    @staticmethod
    def calculate_ear(eye_points):
        A = distance.euclidean(eye_points[1], eye_points[5])
        B = distance.euclidean(eye_points[2], eye_points[4])
        C = distance.euclidean(eye_points[0], eye_points[3])
        if C == 0:
            return 0.0
        return (A + B) / (2.0 * C)

    @staticmethod
    def calculate_mar(mouth_points):
        A = distance.euclidean(mouth_points[1], mouth_points[7])
        B = distance.euclidean(mouth_points[2], mouth_points[6])
        C = distance.euclidean(mouth_points[3], mouth_points[5])
        D = distance.euclidean(mouth_points[0], mouth_points[4])
        if D == 0:
            return 0.0
        return (A + B + C) / (3.0 * D)