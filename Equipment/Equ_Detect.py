import cv2
import math
import cvzone
from ultralytics import YOLO

# Load YOLO model with trained weights
yolo_model = YOLO("Weights/best.pt")  # Adjust the path if needed

# Read the input image
img = cv2.imread("Media/img3.jpg")  # Change the image file as needed

# Define class labels based on your trained model
class_labels = [
    "Swing", "Circular Swing", "Playground", "See-saw", "Slides", 
    "Slide", "Merry-go-round", "Playground-Climbers", "Playground-Climber"
]

# Function to estimate height based on bounding box dimensions
def estimate_height(h, class_name):
    # Approximation logic: Adjust based on real-world data
    if class_name in ["Swing", "Circular Swing", "See-saw", "Merry-go-round"]:
        return round(h * 0.05, 2)  # Example scaling factor
    elif class_name in ["Slides", "Slide", "Playground-Climbers", "Playground-Climber"]:
        return round(h * 0.07, 2)  # Different scaling factor
    else:
        return 0  # Unknown class


# Perform object detection
results = yolo_model(img)

# Loop through detections and draw bounding boxes
for r in results:
    boxes = r.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        w, h = x2 - x1, y2 - y1  # Get width and height of the bounding box

        conf = math.ceil((box.conf[0] * 100)) / 100  # Confidence score
        cls = int(box.cls[0])  # Class index
        class_name = class_labels[cls]  # Get class name

        if conf > 0.3:  # Confidence threshold
            # Estimate height
            height_estimate = estimate_height(h, class_name)
            
            # Draw bounding box
            cvzone.cornerRect(img, (x1, y1, w, h), t=2)
            
            # Label with class name, confidence, and estimated height
            label = f'{class_name} {conf} | {height_estimate} m'
            cvzone.putTextRect(img, label, (max(0, x1), max(35, y1)), scale=1, thickness=1)

# Resize image for better visibility (optional)
img_resized = cv2.resize(img, (800, 600))  # Resize to 800x600 pixels

# Display the image with detections
cv2.imshow("Playground Equipment Detection", img_resized)

# Close window when 'q' is pressed
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
