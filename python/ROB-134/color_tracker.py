from collections import deque
import numpy as np
import cv2 as cv
import imutils
import time
import range_finder as rf


class ColorTracker:
    def __init__(self):
        self.answer = input('Do you want to run the range finder? (y/n): ')
        self.length = 64
        self.frame_width = 1080
        self.min_radius = 10
        self.center = None
        self.minmaxvalues = [111, 191, 94, 132, 255, 203]
        self.cap = cv.VideoCapture(0)
        
        
    def track_color(self):
        
        if self.answer.lower() == 'y':
            self.minmaxvalues = rf.process_live_feed(self.cap, range_filter='hsv', preview=True)
            
        # Define hsv lower and upper bounds
        lower = (self.minmaxvalues[0], self.minmaxvalues[1], self.minmaxvalues[2])
        upper = (self.minmaxvalues[3], self.minmaxvalues[4], self.minmaxvalues[5])
        
        # set up points for tail
        pts = deque(maxlen=self.length)
        
        while True:
            ret, frame = self.cap.read()
            frame = imutils.resize(frame, width=self.frame_width)
            
            # Blur and convert
            blurred = cv.GaussianBlur(frame, (11,11), 0)
            hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
            
            # create mask to errode and dialate
            mask = cv.inRange(hsv, lower, upper)
            #cv.imshow("original", mask)
            mask = cv.erode(mask, None, iterations=2)
            #cv.imshow("erode", mask)
            mask = cv.dilate(mask, None, iterations=2)
            #cv.imshow("dilate", mask)
            
            # find the contours of the image
            cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            center = None
            
            # proceed if atleast one contour
            if len(cnts) > 0:
                # sort by area and take the largest
                c = max(cnts, key=cv.contourArea)
                ((x, y), radius) = cv.minEnclosingCircle(c)
                M = cv.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                
                # proceed if radius is big enough
                if radius > self.min_radius:
                    #draw the graphics 
                    cv.circle(frame, (int(x), int(y)), int(radius), (255,0,0), 2)
                    cv.circle(frame, center, 5, (0,0,255), -1)
                    
                    #print the coordinates
                    print(f'Coordinates: X={center[0]}, Y={center[1]}')
                    
            # update the tail points
            pts.appendleft(center)
            
            # draw the tail
            for i in range(1, len(pts)):
                if pts[i-1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
                cv.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
            
            cv.imshow("Tracker", frame)
            
            key = cv.waitKey(10)
            if key == ord('q'):
                break
        cv.destroyAllWindows()
        print(self.minmaxvalues)
        
        
if __name__ == '__main__':
    ct = ColorTracker()
    ct.frame_width=720
    ct.length= 40
    ct.track_color()
    ct.cap.release()