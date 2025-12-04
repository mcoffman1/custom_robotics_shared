import cv2 as cv
import imutils

camera = cv.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open the camera")
    exit()

print("press 'q' to stop the video feed")

while True:

    #capture a frame
    ret, frame = camera.read()
    frame = imutils.resize(frame, width=1080)

    if not ret:
        print("Error: could not read the frame")
        break

    # Display the image
    cv.imshow("Raw Video Feed", frame)

    # quit if 'q' is pressed
    if cv.waitKey(10) == ord('q'):
        break

# release resources
camera.release()
cv.destroyAllWindows()
