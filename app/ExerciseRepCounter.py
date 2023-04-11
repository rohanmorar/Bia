import cv2
import mediapipe as mp

class ExerciseRepCounter:
    def __init__(self):
        self.started = False
        self.squeezed = False
        self.back_to_start = False
        self.in_progress_of_rep = False
        self.rep_count = 0
        # self.thresholds = {"right_wrist_to_right_hip": 0.15, "right_wrist_to_right_shoulder": 0.3}

    # Returns the distance between two landmarks
    def calculate_distance(self, landmark1, landmark2):
        x1, y1 = landmark1.x, landmark1.y
        x2, y2 = landmark2.x, landmark2.y
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distance

    # Returns the absolute distance between two landmarks in the Y-axis 
    def calculate_distance_y_only(self, landmark1, landmark2):
        y1 = landmark1.y
        y2 = landmark2.y
        distance = abs(y1 - y2)
        return distance

    def process_landmarks(self, landmarks, image = None):
        # Extract relevant landmarks
        right_wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]
        right_hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP]
        right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]

        # Calculate distances between landmarks
        wrist_to_hip_distance = self.calculate_distance(right_wrist, right_hip)
        wrist_to_shoulder_distance = self.calculate_distance(right_wrist, right_shoulder)
    
        if self.started and self.squeezed and self.back_to_start and wrist_to_hip_distance <= 0.175:
            self.rep_count += 1
            if image.any():
                cv2.putText(image, f"REP COUNT: {self.rep_count}", (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (3, 177, 252), 2)
            self.started = False
            self.squeezed = False
            self.back_to_start = False
        elif wrist_to_hip_distance <= 0.1 and self.in_progress_of_rep:
            if image.any():
                cv2.putText(image, "RAISE WEIGHT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            self.back_to_start = True
            self.in_progress_of_rep = False
        elif wrist_to_hip_distance <= 0.2 and not self.in_progress_of_rep:
            if image.any():
                cv2.putText(image, "RAISE WEIGHT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            self.in_progress_of_rep = True
        elif wrist_to_shoulder_distance <= 0.04:
            if image.any():
                cv2.putText(image, "SQUEEZE AT TOP", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            self.squeezed = True
        elif wrist_to_hip_distance >= 0.06 and wrist_to_shoulder_distance > 0.1:
            if image.any():
                cv2.putText(image, f"REP COUNT: {self.rep_count}", (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (3, 177, 252), 2)
            self.started = True
        else:
            if image.any(): 
                cv2.putText(image, f"REP COUNT: {self.rep_count}", (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (3, 177, 252), 2)
        return self.rep_count