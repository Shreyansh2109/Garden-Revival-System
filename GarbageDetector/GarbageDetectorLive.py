import cv2
import math
import cvzone
from ultralytics import YOLO

# Initialize video capture 
cap = cv2.VideoCapture(1)

# Load YOLO model with custom weights
model = YOLO("Weights/best.pt")

# Define class names
classNames = ['0', 'c', 'garbage', 'garbage_bag', 'sampah-detection', 'trash']

# Function to estimate weight based on bounding box dimensions
def estimate_weight(w, h, class_name):
    area = w * h  # Calculate the area of the bounding box
    # Approximation value: adjust these values based on your dataset
    if class_name in ['garbage', 'trash', 'garbage_bag']:
        return round(area * 0.0001, 2)  # scaling factor for garbage
    elif class_name in ['sampah-detection']:
        return round(area * 0.0002, 2)  # scaling factor for sampah-detection
    else:
        return 0  # Unknown class

while True:
    success, img = cap.read()
    
    if not success:
        print("Failed to grab frame")
        break
    
    # Perform object detection
    results = model(img, stream=True)
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            w, h = x2 - x1, y2 - y1
            
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            class_name = classNames[cls]
            
            if conf > 0.1:
                # Estimate weight
                weight = estimate_weight(w, h, class_name)
                
                # Draw bounding box and label
                cvzone.cornerRect(img, (x1, y1, w, h), t=2)
                label = f'{class_name} {conf} | {weight} kg'
                cvzone.putTextRect(img, label, (max(0, x1), max(35, y1)), scale=1, thickness=1)

    # Display the image with detections
    cv2.imshow("Live Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()
