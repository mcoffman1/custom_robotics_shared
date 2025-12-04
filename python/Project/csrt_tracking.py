import cv2
from roi_selection import live_select

# Initialize video capture (0 for default webcam)
cap = cv2.VideoCapture(0)

# Let the user select an ROI on the live feed.
roi_selector = live_select(cap)
if roi_selector is None:
    print("ROI selection canceled or failed.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Get the ROI coordinates from the captured frame.
roi = roi_selector.get_roi()  # Returns (x1, y1, x2, y2)
if roi is None:
    print("No ROI selected.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Convert ROI coordinates to a bounding box (x, y, w, h)
x1, y1, x2, y2 = roi
x = min(x1, x2)
y = min(y1, y2)
w = abs(x2 - x1)
h = abs(y2 - y1)
bbox = (x, y, w, h)

# Initialize the CSRT tracker with the frame captured during ROI selection.
tracker = cv2.TrackerCSRT_create()
initial_frame = roi_selector.image  # The frame used for ROI selection
tracker.init(initial_frame, bbox)

print("Tracker initialized. Starting tracking...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Update the tracker and get updated bounding box coordinates.
    success, bbox = tracker.update(frame)
    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Tracking", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Lost tracking", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (0, 0, 255), 2)

    cv2.imshow("CSRT Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
