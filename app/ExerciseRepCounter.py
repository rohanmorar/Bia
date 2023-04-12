import cv2
import mediapipe as mp

class ExerciseRepCounter:
    def __init__(self, hand):
        self.started = False
        self.squeezed = False
        self.back_to_start = False
        self.in_progress_of_rep = False
        self.rep_count = 0
        self.hand = hand
        self.wrist = None
        self.hip = None
        self.shoulder = None
        print(self.hand)

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

    # Sets the classes instance variables of wrist, hip, and shoulder, to the respective landmark based on left/right hand selection
    def set_this_exercises_landmarks_based_on_hand_chosen(self, landmarks):
        if self.hand == 'right':
            self.wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]
            self.hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP]
            self.shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
        elif self.hand == 'left':
            self.wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST]
            self.hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP]
            self.shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
        # else:
        #     raise ValueError(f"Invalid hand argument: {self.hand}. Please use either 'left' or 'right'.")

    def process_landmarks(self, landmarks, image = None):
        # Set up the landmarks for use
        self.set_this_exercises_landmarks_based_on_hand_chosen(landmarks)

        # Calculate distances between landmarks
        wrist_to_hip_distance = self.calculate_distance(self.wrist, self.hip)
        wrist_to_shoulder_distance = self.calculate_distance(self.wrist, self.shoulder)
    
        """ Rep tracking and incrementing logic for ISOLATED DUMBELL CURL
            TODO: allow for different track/increment logic based on excercise selection
        """ 
        if self.started and self.squeezed and self.back_to_start and wrist_to_hip_distance <= 0.175:
            self.rep_count += 1
            if image.any():
                cv2.putText(image, f"{self.hand.upper()} HANDED REP COUNT: {self.rep_count}", (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (3, 177, 252), 2)
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
                cv2.putText(image, f"{self.hand.upper()} HANDED REP COUNT: {self.rep_count}", (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (3, 177, 252), 2)
            self.started = True
        else:
            if image.any(): 
                cv2.putText(image, f"{self.hand.upper()} HANDED REP COUNT: {self.rep_count}", (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (3, 177, 252), 2)
        return self.rep_count