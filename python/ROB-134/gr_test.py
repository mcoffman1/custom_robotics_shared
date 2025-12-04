import gesture_recognition as gr
import cv2 as cv

cap = cv.VideoCapture(0)

# Use spacebar to store gestures, and 'q' when all gestures have been recorded.
gestures = gr.store_gestures(cap, threshold=0.2)
# print("==============================================================")
# print(f"List = {gestures}")
# print("==============================================================")

# Process live feed and show which gesture is detected (press 's' to stop).
gr.detect(cap, gestures, threshold=0.1)

cap.release()
cv.destroyAllWindows()