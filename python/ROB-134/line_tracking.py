import cv2
import numpy as np
import math
import range_finder  # Import your custom range_finder module for trackbar-based HSV calibration

def process_frame(frame, lower, upper, range_filter='HSV'):
    """
    Process the given frame to detect a colored line, choose the endpoint closest to the top
    of the image, and compute control commands (linear and angular velocities) based on a vector
    drawn from the center of the screen to that endpoint.
    
    Args:
        frame: The original BGR frame.
        lower: NumPy array with lower HSV bounds.
        upper: NumPy array with upper HSV bounds.
        range_filter: The color space used for thresholding ('HSV' is expected).
    
    Returns:
        The processed frame with the detected line and the control vector drawn.
    """
    # Convert to the chosen color space.
    if range_filter.upper() == 'HSV':
        frame_to_thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    else:
        frame_to_thresh = frame

    # Apply the HSV threshold.
    mask = cv2.inRange(frame_to_thresh, lower, upper)
    
    # (Optional) Clean up the mask with morphological operations.
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Detect edges using Canny.
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    
    # Use the probabilistic Hough Transform to detect line segments.
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50,
                            minLineLength=50, maxLineGap=10)

    height, width = frame.shape[:2]
    center_x = width // 2
    center_y = height // 2

    if lines is not None:
        # Select the longest line segment.
        longest_line = None
        max_length = 0
        for line in lines:
            for x1, y1, x2, y2 in line:
                length = math.hypot(x2 - x1, y2 - y1)
                if length > max_length:
                    max_length = length
                    longest_line = (x1, y1, x2, y2)
                    
        if longest_line is not None:
            x1, y1, x2, y2 = longest_line

            # Draw the detected line (green) for visualization.
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            
            # Choose the endpoint that is closest to the top (i.e. smallest y value).
            if y1 < y2:
                target_point = (x1, y1)
            else:
                target_point = (x2, y2)

            tx, ty = target_point

            # Draw a circle at the selected target point.
            cv2.circle(frame, target_point, 5, (0, 0, 255), -1)

            # Draw a vector (arrow) from the center of the image to the target point.
            cv2.arrowedLine(frame, (center_x, center_y), target_point, (255, 0, 0), 2)

            # Compute the differences relative to the center.
            error_x = tx - center_x       # horizontal difference (for turning)
            error_y = center_y - ty       # vertical difference (for forward/reverse)
                                         # (Note: if ty is above center, error_y is positive)

            # Compute control commands:
            # - Linear velocity: proportional to how far the target is above the center.
            #   (If the target is below the center, this value becomes negative for reverse.)
            k_linear = 0.005  # Tune this constant as needed.
            v = k_linear * error_y

            # - Angular velocity: proportional to the horizontal offset.
            k_turn = 0.005    # Tune this constant as needed.
            w = k_turn * error_x

            print(f"Target point: {target_point}, error_x: {error_x}, error_y: {error_y}")
            print(f"Command velocities: linear = {v:.2f}, angular = {w:.2f}")

    else:
        print("No line detected.")

    return frame

def main():
    # Open the video capture.
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # --- CALIBRATION USING THE range_finder MODULE ---
    # Launch the live feed calibration with HSV trackbars.
    # Adjust the HSV thresholds until the colored line is isolated, then press SPACE.
    print("Calibrating color threshold using range_finder...")
    track_vals = range_finder.process_live_feed(cap, range_filter='HSV', preview=True, imutils=False, frame_width=640)
    # The returned list is expected to be:
    # [v1_min, v2_min, v3_min, v1_max, v2_max, v3_max]
    lower = np.array(track_vals[0:3])
    upper = np.array(track_vals[3:6])
    print(f"Calibration complete: lower = {lower}, upper = {upper}")
    
    # --- MAIN LOOP FOR LINE TRACKING ---
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        processed_frame = process_frame(frame, lower, upper, range_filter='HSV')
        cv2.imshow("Line Tracking", processed_frame)
        
        # Press 'q' to quit.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
