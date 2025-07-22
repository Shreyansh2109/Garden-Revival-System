import cv2
import math
import cvzone
from ultralytics import YOLO

# Load YOLO model with custom weights
yolo_model = YOLO("Weights/best.pt")

# Read the input image
img = cv2.imread("Media/garbage_5.jpeg")

# Define class names
class_labels = ['0', 'c', 'garbage', 'garbage_bag', 'sampah-detection', 'trash']

## Function to estimate weight based on bounding box dimensions
def estimate_weight(w, h, class_name):
    area = w * h  # Calculate the area of the bounding box
    
    # Adjust the scaling factors to get a smaller weight
    if class_name in ['garbage', 'trash', 'garbage_bag']:
        # Further reduced scaling factor for garbage-related classes to get smaller weights
        return round(area * 0.00002, 2)  # Adjusted scaling factor for garbage
    elif class_name in ['sampah-detection']:
        # Adjusted scaling factor for sampah-detection
        return round(area * 0.00005, 2)  # Slightly smaller factor for sampah-detection
    else:
        return 0  # Unknown class



# Perform object detection
results = yolo_model(img)

# Loop through the detections and draw bounding boxes
for r in results:
    boxes = r.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        w, h = x2 - x1, y2 - y1

        conf = math.ceil((box.conf[0] * 100)) / 100
        cls = int(box.cls[0])
        class_name = class_labels[cls]

        if conf > 0.3:
            # Estimate weight
            weight = estimate_weight(w, h, class_name)
            cvzone.cornerRect(img, (x1, y1, w, h), t=2)
            label = f'{class_name} {conf} | {weight} kg'
            cvzone.putTextRect(img, label, (max(0, x1), max(35, y1)), scale=1, thickness=1)

# Resize the image for better visibility (optional, adjust dimensions as needed)
img_resized = cv2.resize(img, (800, 600))  # Resize to 800x600 pixels or another resolution

# Display the image with detections
cv2.imshow("Image", img_resized)

# Close window when 'q' button is pressed
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
