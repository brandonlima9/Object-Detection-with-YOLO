import cv2  # Importing OpenCV for video capture and image processing
from ultralytics import YOLO  # Import YOLO model for object detection
from viz import draw_detect  # Import the custom function to draw bounding boxes

import torch

# Check if MPS (Metal Performance Shaders) is available on your Mac's GPU
# Check if CUDA is available on you PC's GPU
# if neither use CPU
if torch.cuda.is_available():
    device = 'cuda'
elif torch.backends.mps.is_available():
    device = 'mps'
else: 
    device = 'cpu'

# Load the custom trained model from the directory
model = YOLO('./best.pt')
# Move the model to the appropriate device (GPU or CPU)
model.to(device)
print(f"Using device: {device}")

# Open the video stream (camera input)
stream = cv2.VideoCapture(0)  # 1 refers to the camera device index, '0' is the default webcam

# Define the list of objects we want to detect (class indices)
objects = [0]  # Class ID for 'package'
names = ['package', 'polybag']  # List of object names

# Initialize 'ret' as True, which will control the loop
ret = True

while ret:
    ret, frame = stream.read()  # Read a frame from the video stream

    # Perform object detection on the current frame
    # Run the frame through the YOLO model and move to device
    detections = model(frame)[0].cpu()  # Ensure the result is moved back to CPU if needed

    # Iterate over the detections and draw bounding boxes around detected objects
    for detection in detections.boxes.data.tolist():  # Get the bounding boxes and their details
        x1, y1, x2, y2, score, class_id = detection  # Unpack the box coordinates, score, and class ID

        if int(class_id) in objects:  # Check if the detected class is in our list of objects to detect
            # Call the draw_border function to draw the bounding box around the object
            draw_detect(frame, names[int(class_id)], int(x1), int(y1), int(x2), int(y2), (0, 255, 0), 10)

    # Display the frame with the bounding boxes in a window named 'Capture'
    cv2.imshow('Capture', frame)

    # Break the loop if the user presses the 'q' key while the python application is in the foreground
    if cv2.waitKey(1) == ord('q'):  # Wait for 1 ms and check if the 'q' key is pressed
        break  # Exit the loop if 'q' is pressed

# Release the video capture object and close all OpenCV windows
stream.release()
cv2.destroyAllWindows()  # Close the OpenCV window
