import cv2
import numpy as np
import time

# Use raw string for the file path or double backslashes
bgpic_path = 'c:\\Users\\mcoffman1\\OneDrive - WSUTech\\MATTHEW\\Robotics\\Python\\images\\mountains.jpeg'

# Attempt to load the background picture
bgpic = cv2.imread(bgpic_path)
if bgpic is None:
    raise ValueError(f"Unable to load the background image from the path: {bgpic_path}")

# Initialize the trackbar values
lower_bound = np.array([0, 0, 0])
upper_bound = np.array([0, 0, 0])

count = 0
maxcount = 3

# This callback function updates the HSV range values
def get_values(x):
    global lower_bound, upper_bound
    hueLow = cv2.getTrackbarPos('Blow', 'Trackbars')
    hueUp = cv2.getTrackbarPos('Bupp', 'Trackbars')
    Ls = cv2.getTrackbarPos('Glow', 'Trackbars')
    Us = cv2.getTrackbarPos('Gupp', 'Trackbars')
    Lv = cv2.getTrackbarPos('Rlow', 'Trackbars')
    Uv = cv2.getTrackbarPos('Rupp', 'Trackbars')

    lower_bound = np.array([hueLow, Ls, Lv])
    upper_bound = np.array([hueUp, Us, Uv])

# Create a window named 'Trackbars' with trackbars for adjusting HSV range
cv2.namedWindow('Trackbars')
cv2.createTrackbar('Blow', 'Trackbars', 0, 255, get_values)
cv2.createTrackbar('Bupp', 'Trackbars', 255, 255, get_values)
cv2.createTrackbar('Glow', 'Trackbars', 0, 255, get_values)
cv2.createTrackbar('Gupp', 'Trackbars', 255, 255, get_values)
cv2.createTrackbar('Rlow', 'Trackbars', 0, 255, get_values)
cv2.createTrackbar('Rupp', 'Trackbars', 255, 255, get_values)

# If you want to switch to video later, just uncomment the following lines
# cap = cv2.VideoCapture(0)

# Uncomment this if you are using a video feed
# if not cap.isOpened():
#     print("Error: Could not open video capture.")
#     exit()

# Use a video feed or a static image
using_video = False  # Change to True when using video

while True:
    # If using a video feed, read a new frame
    if using_video:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from the video stream.")
            break
    else:
        # Load the foreground picture each iteration to reset any drawing on the image
        time.sleep(.1)
        
        fgpic_path = 'c:\\Users\\mcoffman1\\OneDrive - WSUTech\\MATTHEW\\Robotics\\Python\\images\\boot.jpg'
        fgpic = cv2.imread(fgpic_path)
        if fgpic is None:
            raise ValueError(f"Unable to load the foreground image from the path: {fgpic_path}")
        
        
    count += 1
    if count > maxcount:
        count = 0
    elif count < maxcount:
        pass
    else:
        # Ensure the background is resized to match the foreground dimensions
        fgpic = cv2.resize(fgpic, (bgpic.shape[1], bgpic.shape[0]))


        # Convert foreground image to HSV
        #hsv = cv2.cvtColor(fgpic, cv2.COLOR_BGR2HSV)
        bgr = fgpic

        # Create a mask with the current HSV range
        mask = cv2.inRange(bgr, lower_bound, upper_bound)
        mask_inv = cv2.bitwise_not(mask)

        # Extract the foreground and background regions based on the mask
        fg = cv2.bitwise_and(fgpic, fgpic, mask=mask_inv)
        bg = cv2.bitwise_and(bgpic, bgpic, mask=mask)

        # Combine both the foreground and the background to create the final image
        combined = cv2.add(fg, bg)
        
        #cv2.imshow('fg', fg)  # Original image
        #cv2.imshow('bg', bg)  # The mask created from HSV range

        #cv2.imshow('Frame', fgpic)  # Original image
        cv2.imshow('Mask', mask)  # The mask created from HSV range
        cv2.imshow('Combined', combined)  # The final image with background replaced

    if cv2.waitKey(1) == ord('q'):
        break

# If using a video feed, release the capture device
if using_video:
    cap.release()

cv2.destroyAllWindows()
