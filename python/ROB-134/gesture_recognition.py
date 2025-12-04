# gesture_recognition.py

import cv2
import mediapipe as mp
import math

# Initialize MediaPipe objects.
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def get_hands():
    """Return a new MediaPipe Hands instance."""
    return mp_hands.Hands(min_detection_confidence=0.5, 
                          min_tracking_confidence=0.5)

def get_gesture_signature(landmarks):
    """
    Compute a gesture signature using a richer set of finger landmarks.

    The signature is normalized for:
      - Translation (wrist at origin),
      - Scale (dividing by the distance from wrist to middle finger tip),
      - Rotation (rotating so the vector from wrist to middle finger tip
        is aligned along the positive X-axis).

    Instead of using only the fingertips, we now use all finger-related
    landmarks (indices 1 through 20). The coordinates are rounded to two decimal places.
    """
    wrist = landmarks.landmark[0]
    indices = list(range(1, 21))  # use landmarks 1 through 20
    middle_tip = landmarks.landmark[12]
    
    # Compute reference angle (wrist to middle finger tip).
    ref_angle = math.atan2(middle_tip.y - wrist.y, middle_tip.x - wrist.x)
    
    # Compute scale as the distance from wrist to middle finger tip.
    scale = math.sqrt((middle_tip.x - wrist.x) ** 2 + (middle_tip.y - wrist.y) ** 2)
    if scale == 0:
        scale = 1e-6  # safeguard against division by zero

    signature = []
    for i in indices:
        point = landmarks.landmark[i]
        # Translate: get coordinates relative to the wrist.
        dx = (point.x - wrist.x) / scale
        dy = (point.y - wrist.y) / scale
        # Rotate: normalize for hand rotation.
        cos_theta = math.cos(-ref_angle)
        sin_theta = math.sin(-ref_angle)
        norm_x = dx * cos_theta - dy * sin_theta
        norm_y = dx * sin_theta + dy * cos_theta
        signature.append((round(norm_x, 2), round(norm_y, 2)))
    return tuple(signature)

def gesture_distance(sig1, sig2):
    """
    Compute the average Euclidean distance between two gesture signatures.
    Each signature is a tuple of (x, y) points.
    """
    distances = []
    for (x1, y1), (x2, y2) in zip(sig1, sig2):
        distances.append(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
    return sum(distances) / len(distances)

def store_gestures(cap, threshold=0.2):
    """
    Record gestures from the provided video capture device.

    Use the spacebar to capture a still image and store the gesture.
    Press 'q' to finish recording.

    Parameters:
        cap: OpenCV VideoCapture object.
        threshold: (Not used during storage, but provided for interface consistency.)

    Returns:
        A list of recorded gestures as tuples (signature, label).
    """
    recorded_gestures = []
    hands = get_hands()
    window_name = "Store Gestures"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip for mirror effect and convert to RGB.
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        cv2.putText(frame, "Press SPACE to store gesture, 'q' to finish", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # SPACE key
            if results.multi_hand_landmarks:
                # Use the first detected hand.
                hand_landmarks = results.multi_hand_landmarks[0]
                signature = get_gesture_signature(hand_landmarks)
                label = input("Enter name for this gesture: ")
                recorded_gestures.append((signature, label))
                print(f"Gesture '{label}' recorded with signature: {signature}")
        elif key == ord('q'):
            break

    hands.close()
    cv2.destroyWindow(window_name)
    return recorded_gestures

def detect(cap, gestures, threshold=0.2):
    """
    Process live video feed and detect recorded gestures.

    The function compares the current gesture signature against all stored signatures.
    If a match is found (based on the threshold), the label is displayed.
    Press 's' to stop detection.

    Parameters:
        cap: OpenCV VideoCapture object.
        gestures: List of recorded gestures (each as a tuple (signature, label)).
        threshold: Matching threshold (average Euclidean distance).
    """
    hands = get_hands()
    window_name = "Gesture Detection"
    last_printed_gesture = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                current_signature = get_gesture_signature(hand_landmarks)
                recognized_label = None
                min_distance = None
                for recorded_sig, label in gestures:
                    dist = gesture_distance(current_signature, recorded_sig)
                    if dist < threshold:
                        if recognized_label is None or dist < min_distance:
                            recognized_label = label
                            min_distance = dist
                if recognized_label is not None:
                    # Move the gesture label down (e.g., to y=80) and change its color to red (BGR: (0, 0, 255))
                    cv2.putText(frame, recognized_label, (50, 80), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    if recognized_label != last_printed_gesture:
                        print("Detected gesture:", recognized_label)
                        last_printed_gesture = recognized_label
                else:
                    last_printed_gesture = None
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the stop message at the top.
        cv2.putText(frame, "Press 's' to stop detection", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            break

    hands.close()
    cv2.destroyWindow(window_name)
