import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Define a function to calculate the distance between two landmarks
def calculate_distance(landmark1, landmark2):
    x1, y1 = landmark1.x, landmark1.y
    x2, y2 = landmark2.x, landmark2.y
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance

# Define a function to calculate the distance between two landmarks
def calculate_distance_y_only(landmark1, landmark2):
    y1 = landmark1.y
    y2 = landmark2.y
    distance = abs(y1 - y2)
    return distance

# Set up Mediapipe Pose for landmark detection
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    # Set up video capture
    cap = cv2.VideoCapture(0)

    # Initialize variables for rep counting
    rep_count = 0
    in_starting_pos = False
    raising_weight = False
    squeezing_muscle = False
    in_progress_of_rep = False

    started, squeezed, back_to_start = False, False, False

    while cap.isOpened():
        # Read frame from video capture
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert image to RGB for Mediapipe
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process image with Mediapipe Pose
        results = pose.process(image)

        # Draw pose landmarks on image
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
        except AttributeError:
            continue

        # Extract relevant landmarks
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # Calculate distances between landmarks
        wrist_to_hip_distance = calculate_distance(right_wrist, right_hip)
        wrist_to_shoulder_distance = calculate_distance(right_wrist, right_shoulder)
        # wrist_to_hip_distance_Y_only = calculate_distance_y_only(right_wrist, right_shoulder)
        
        if started and squeezed and back_to_start and wrist_to_hip_distance <= 0.175:
            rep_count += 1
            cv2.putText(image, f"REP COUNT: {rep_count}", (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (3, 177, 252), 2)
            started = False
            squeezed = False
            back_to_start = False
        elif wrist_to_hip_distance <= 0.1 and in_progress_of_rep:
            cv2.putText(image, "RAISE WEIGHT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            back_to_start = True
            in_progress_of_rep = False
        elif wrist_to_hip_distance <= 0.2 and not in_progress_of_rep:
            cv2.putText(image, "RAISE WEIGHT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            in_progress_of_rep = True
        elif wrist_to_shoulder_distance <= 0.04:
            cv2.putText(image, "SQUEEZE AT TOP", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            squeezed = True    
        elif wrist_to_hip_distance >= 0.06 and wrist_to_shoulder_distance > 0.1:
            cv2.putText(image, f"REP COUNT: {rep_count}", (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (3, 177, 252), 2)
            started = True
        else:
            cv2.putText(image, f"REP COUNT: {rep_count}", (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (3, 177, 252), 2)

        # Display image
        cv2.imshow('Pose detection', image)

        # Exit on ESC
        if cv2.waitKey(5) & 0xFF == 27:
            break

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()