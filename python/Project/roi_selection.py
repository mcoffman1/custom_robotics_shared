import cv2
import numpy as np

class ROISelector:
    HEADER_HEIGHT = 40  # Height in pixels for the instruction bar

    def __init__(self, image):
        self.image = image
        self.ref_point = []
        self.cropping = False
        self.roi_coords = None
        self.display_copy = self.add_instructions(self.image.copy(), 
                                                  "Click and drag to select ROI. Press SPACE to confirm or 'q' to quit.")

    def add_instructions(self, img, text):
        """
        Draw a header bar with instructions at the top of the image.
        """
        overlay = img.copy()
        # Draw a filled rectangle as the header bar
        cv2.rectangle(overlay, (0, 0), (img.shape[1], self.HEADER_HEIGHT), (50, 50, 50), thickness=cv2.FILLED)
        # Put white text over the bar
        cv2.putText(overlay, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return overlay

    def click_and_drag(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Start the ROI selection
            self.ref_point = [(x, y)]
            self.cropping = True

        elif event == cv2.EVENT_MOUSEMOVE and self.cropping:
            # Show the rectangle while dragging
            temp = self.image.copy()
            cv2.rectangle(temp, self.ref_point[0], (x, y), (0, 255, 0), 2)
            self.display_copy = self.add_instructions(temp, 
                "Drawing ROI: Release mouse to finish. Press SPACE to confirm or 'q' to quit.")

        elif event == cv2.EVENT_LBUTTONUP and self.cropping:
            # Finalize the ROI drawing
            self.ref_point.append((x, y))
            self.cropping = False
            temp = self.image.copy()
            cv2.rectangle(temp, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
            self.roi_coords = (self.ref_point[0][0], self.ref_point[0][1],
                               self.ref_point[1][0], self.ref_point[1][1])
            self.display_copy = self.add_instructions(temp, 
                "ROI drawn. Press SPACE to confirm or 'q' to cancel.")

    def get_roi(self):
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", self.click_and_drag)

        while True:
            cv2.imshow("Image", self.display_copy)
            key = cv2.waitKey(1) & 0xFF

            if key == 32:  # SPACE key confirms selection if ROI exists
                if self.roi_coords is not None:
                    break
            elif key == ord('q'):
                self.roi_coords = None
                break

        cv2.destroyAllWindows()
        return self.roi_coords


def image_select(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error: Image not found.")
    return ROISelector(image)


def live_select(cap):
    window_name = "Live Feed"
    cv2.namedWindow(window_name)
    while True:
        ret, frame = cap.read()
        if not ret:
            raise ValueError("Error: Could not capture frame.")

        # Add a header bar with instructions for the live feed
        header_height = 40
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (frame.shape[1], header_height), (50, 50, 50), thickness=cv2.FILLED)
        cv2.putText(overlay, "Live Feed: Press SPACE to capture frame, or 'q' to quit.",
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow(window_name, overlay)
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # SPACE key to capture frame
            cv2.destroyWindow(window_name)
            # Start ROI selection on the captured frame
            return ROISelector(frame)
        elif key == ord('q'):
            cv2.destroyAllWindows()
            return None
