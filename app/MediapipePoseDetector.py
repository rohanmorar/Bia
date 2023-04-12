import mediapipe as mp
import cv2

# MediapipePoseDetector class will be responsible for mediapose related setup
class MediapipePoseDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def process_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return results
