import cv2 as cv
import imutils
import time

cap = cv.VideoCapture(0)
time.sleep(2)

# set the dimensions of my pic
#cap.set(cv.CAP_PROP_FRAME_WIDTH, 480)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=1080)
    cv.imshow("Spacebar to Capture",frame)
    key = cv.waitKey(1)
    if key == ord(' '):
        break
# take frame
ret, frame = cap.read()
frame = imutils.resize(frame, width=1080)

# write image to a file
cv.imwrite('sample_image.jpg',frame)

cap.release()