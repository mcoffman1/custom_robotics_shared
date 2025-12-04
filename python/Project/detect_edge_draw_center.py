import cv2
import numpy as np
import roi_selection  # Import the ROI selection module

def process_image(image_path):
    # Load the full original image and create a copy for drawing.
    image = cv2.imread(image_path)
    output = image.copy()

    # Use image_select to let the user choose an ROI on the full image.
    selector = roi_selection.image_select(image_path)
    roi_coords = selector.get_roi()
    
    if roi_coords is None:
        print("No ROI selected.")
        return None

    # Unpack ROI coordinates.
    (x1, y1, x2, y2) = roi_coords

    # Extract the ROI region for processing (without cropping the display image).
    roi = image[y1:y2, x1:x2]
    
    # Process the ROI: convert to grayscale, blur, and apply Canny edge detection.
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours on the edge-detected ROI.
    contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Offset the contours so they are drawn in the correct location on the full image.
    offset_contours = []
    for cnt in contours:
        cnt_offset = cnt + [x1, y1]  # Apply the ROI offset
        offset_contours.append(cnt_offset)
    
    # Draw all detected contours in blue (BGR: blue is (255, 0, 0)) on the output image.
    cv2.drawContours(output, offset_contours, -1, (255, 0, 0), 2)
    
    # For the largest contour, compute its centroid and draw it in red (BGR: red is (0, 0, 255)).
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"]) + x1  # Adjust centroid x-coordinate with ROI offset.
            cY = int(M["m01"] / M["m00"]) + y1  # Adjust centroid y-coordinate with ROI offset.
            cv2.circle(output, (cX, cY), 5, (0, 0, 255), -1)
        else:
            print("Largest contour has zero area; cannot compute centroid.")
    else:
        print("No contours found.")
    
    # Optionally, draw the ROI rectangle on the full image for reference.
    cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    return output

def main():
    image_path = "sample_image.jpg"
    
    while True:
        processed_image = process_image(image_path)
        if processed_image is None:
            break
        
        cv2.imshow("Detected Object with Edges", processed_image)
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord('q'):
            break
        elif key == 32:  # SPACE key pressed: restart the process.
            cv2.destroyAllWindows()
            continue

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
