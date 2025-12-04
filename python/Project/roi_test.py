import roi_selection
import cv2 as cv
import time

# **Live Feed Selection**
cap = cv.VideoCapture(0)  # Open camera
time.sleep(2)  # Give the camera time to adjust

live = roi_selection.live_select(cap)  # Start live ROI selection
if live:
    box_coords = live.get_roi()  # Get ROI coordinates
    print("Live Feed ROI Coordinates:", box_coords)

cap.release()  # Release the camera

# **Image Selection**
image_path = "sample_image.jpg"
still = roi_selection.image_select(image_path)  # Start image ROI selection
box_coords = still.get_roi()  # Get ROI coordinates
print("Image ROI Coordinates:", box_coords)
