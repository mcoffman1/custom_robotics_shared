import cv2
import imutils as im


def callback(value):
    pass


def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255
        for j in range_filter:
            cv2.createTrackbar(f"{j}_{i}","Trackbars", v, 255, callback)


def get_trackbar_values(range_filter):

    values = []
    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos(f"{j}_{i}", "Trackbars")
            values.append(v)
    return values


def process_live_feed(camera, range_filter='BGR', preview=True, imutils=False, frame_width=1280):
    """
    Process live feed from the webcam and return threshold values.
    :param camera: camera connection created using imutils or cv2
    :param range_filter: 'RGB' or 'HSV' for thresholding.
    :param preview: Whether to show a preview of the masked image.
    :param imutils: If using imutils set this to True\
    :param 
    :return: List of trackbar values [v1_min, v2_min, v3_min, v1_max, v2_max, v3_max].
    """

    setup_trackbars(range_filter.upper())

    while True:
        if imutils:
            frame = camera.read()
        else:
            ret, frame = camera.read()
        frame = im.resize(frame, width=frame_width)

        if range_filter.upper() == 'HSV':
            frame_to_thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        else:
            frame_to_thresh = frame

        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter.upper())

        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        if preview:
            preview_image = cv2.bitwise_and(frame, frame, mask=thresh)
            cv2.imshow("Preview", preview_image)
        else:
            cv2.imshow("Original", frame)
            cv2.imshow("Thresh", thresh)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # spacebar to save and exit
            break

    cv2.destroyAllWindows()

    return [v1_min, v2_min, v3_min, v1_max, v2_max, v3_max]


def process_image(image_path, range_filter='BGR', preview=True, frame_width=1080):
    """
    Apply thresholding to a static image and return threshold values.
    :param image_path: Path to the input image.
    :param range_filter: 'RGB' or 'HSV' for thresholding.
    :param preview: Whether to show a preview of the masked image.
    :return: List of trackbar values [v1_min, v2_min, v3_min, v1_max, v2_max, v3_max].
    """
    image = cv2.imread(image_path)
    image = im.resize(image, width=frame_width)
    
    if image is None:
        raise ValueError("Image not found at specified path.")

    if range_filter.upper() == 'HSV':
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    else:
        frame_to_thresh = image

    setup_trackbars(range_filter.upper())

    while True:
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter.upper())

        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        if preview:
            preview_image = cv2.bitwise_and(image, image, mask=thresh)
            cv2.imshow("Preview", preview_image)
        else:
            cv2.imshow("Original", image)
            cv2.imshow("Thresh", thresh)

        key = cv2.waitKey(1)
        if key == ord(' '):
            break
    
    cv2.destroyAllWindows()

    return [v1_min, v2_min, v3_min, v1_max, v2_max, v3_max]