import cv2 as cv
import numpy as np
from imutils.video import VideoStream
import imutils

def canny_webcam():
    # Initialize webcam stream
    cap = VideoStream(src=0).start()
    edgeshow = -1  # Toggle variable for showing edges

    print("Press SPACE to toggle edge detection view.")
    print("Press 'q' to quit.")

    try:
        while True:
            # Read a frame from the webcam
            frame = cap.read()
            if frame is None:
                print("Failed to read frame from webcam.")
                break
            
            # Resize frame for consistency
            frame = imutils.resize(frame, width=1080)

            # Apply Canny edge detection
            edge = cv.Canny(frame, 65, 100)

            # Toggle view based on the spacebar toggle
            if edgeshow == 1:
                cv.imshow('Canny Edge', edge)
            else:
                cv.imshow('Canny Edge', frame)

            # Handle keyboard inputs
            key = cv.waitKey(10)
            if key == ord(' '):  # Toggle edge view
                edgeshow *= -1
            elif key == ord('q'):  # Quit program
                break
    finally:
        # Release resources
        cap.stop()
        cv.destroyAllWindows()

if __name__ == "__main__":
    canny_webcam()
