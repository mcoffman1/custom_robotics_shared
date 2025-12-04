import cv2
import os
import time

# Specify your folder path here
folder_path = "c:\\Users\\mcoffman1\\OneDrive - WSUTech\\MATTHEW\\Robotics\\Python\\images"
# Get a list of file names in the folder
images = []

def display_images_in_folder(folder_path):
    for img in os.listdir(folder_path):
        if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            images.append(img)

    for image_name in images:
        image_path = os.path.join(folder_path, image_name)

        # Read and display the image
        img = cv2.imread(image_path)
        if img is not None:
            cv2.imshow('Image', img)
            cv2.waitKey(1000)  # Display each image for 1000 milliseconds (1 second)
        else:
            print(f"Error loading image {image_path}")

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

display_images_in_folder(folder_path)
