import cv2 # type: ignore
import os

# Open the camera (0 is usually the default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

#Capture a frame
ret, frame = cap.read()

if not ret:
    print("Failed to grab frame.")
else:
    # Show the frame in a window
    cv2.imshow('Captured Image', frame)

    # Create a directory for saving images if it doesn't exist
    directory = 'captured_images'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the path and filename to save the image
    filename = os.path.join(directory, 'captured_image.jpg')

    # Save the captured image
    cv2.imwrite(filename, frame)
    print(f"Image saved to {filename}")

# Wait for a key press to close the image window
cv2.waitKey(0)

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
