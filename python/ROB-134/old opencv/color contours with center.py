import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.createTrackbar('hueLower', 'Trackbars', 50, 255, nothing)
cv2.createTrackbar('hueUpper', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('satLow', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('satHigh', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('valLow', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('valHigh', 'Trackbars', 255, 255, nothing)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get HSV value range from the trackbars
    hueLow = cv2.getTrackbarPos('hueLower', 'Trackbars')
    hueUp = cv2.getTrackbarPos('hueUpper', 'Trackbars')
    Ls = cv2.getTrackbarPos('satLow', 'Trackbars')
    Us = cv2.getTrackbarPos('satHigh', 'Trackbars')
    Lv = cv2.getTrackbarPos('valLow', 'Trackbars')
    Uv = cv2.getTrackbarPos('valHigh', 'Trackbars')

    lower_bound = np.array([hueLow, Ls, Lv])
    upper_bound = np.array([hueUp, Us, Uv])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Find contours
    (contours, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Filter out small contours (noise)
        filtered_contours = [c for c in contours if cv2.contourArea(c) > 10]

        if filtered_contours:
            # Find the largest contour
            largest_contour = max(filtered_contours, key=cv2.contourArea)

            # Calculate the moments of the largest contour
            M = cv2.moments(largest_contour)

            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # (cx, cy) are the coordinates of the center of the object

                # Draw the largest contour
                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)

                # Draw a red circle at the center
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
