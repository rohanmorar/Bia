import cv2
import mediapipe as mp
import ExerciseRepCounter
import MediapipePoseDetector
import sys
import time

running, hand_choice = True, None

# hand_choice = sys.argv[1]
pose_detector = MediapipePoseDetector.MediapipePoseDetector()
isolated_bicep_curl_rep_counter = ExerciseRepCounter.ExerciseRepCounter('right') # hand_choice

cap = cv2.VideoCapture(0)


while cap.isOpened():
    # Read frame from video capture
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert image to RGB for Mediapipe
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process image with Mediapipe Pose
    results = pose_detector.pose.process(image)

    # Draw pose landmarks on image
    #pose_detector.mp_drawing.draw_landmarks(image, results.pose_landmarks, pose_detector.mp_pose.POSE_CONNECTIONS)

    # Extract landmarks
    try:
        landmarks = results.pose_landmarks.landmark
    except AttributeError:
        continue

    # Process landmarks with exercise rep counter
    rep_count = isolated_bicep_curl_rep_counter.process_landmarks(landmarks, image)

    # Display image
    cv2.imshow('Pose detection', image)

    # Exit on ESC
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()