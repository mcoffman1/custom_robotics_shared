import cv2 as cv
from imutils.video import VideoStream
import range_finder as rf 

cap = cv.VideoCapture(0)
#cap = VideoStream(src=0).start()

minmax = rf.process_live_feed(cap, preview=True, frame_width=720)
print(minmax)

#minmax = rf.process_image('images\\image.jpg', range_filter='hsv', frame_width=720)
#print(minmax)

cap.release()
#cap.stop()

#c:\\Users\\mcoffman1\\OneDrive - WSUTech\\MATTHEW\\Director Documents\\WSU Tech courses\\ROB-134\\