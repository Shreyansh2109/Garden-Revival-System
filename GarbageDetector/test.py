import cv2
import math
import cvzone
from ultralytics import YOLO
from pymongo import MongoClient
from datetime import datetime

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://sshreyansh2103:sshreyansh2103@cluster0.p58xg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["test"]  # Database name
collection = db["garbagecollections"]  # Collection name
print("Connected to MongoDB Atlas successfully!")

# Initialize video capture
cap = cv2.VideoCapture(1)

# Load YOLO model with custom weights
model = YOLO("Weights/best.pt")

# Define class names (only garbage-related classes are considered)
classNames = ['0', 'c', 'garbage', 'garbage_bag', 'sampah-detection', 'trash']

# Function to estimate weight
def estimate_weight(w, h):
    area = w * h  # Bounding box area
    weight = round(((math.sqrt(area) / 70) + 0.1) * 0.8, 2)  # Adjusted formula
    return max(weight, 0.05)  # Ensure weight is not too low

frame_id = 0  # Track frame number
tracked_objects = {}  # Stores last detected frame for each garbage type

while True:
    success, img = cap.read() #Reads a frame from the webcam
    frame_id += 1  # Increment frame count

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

            # Only process 'garbage', 'garbage_bag', and 'trash'
            if conf > 0.1 and class_name in ['garbage', 'garbage_bag', 'trash']:
                weight = estimate_weight(w, h)

                # Avoid duplicate counting for the same object in consecutive frames
                if class_name not in tracked_objects or frame_id - tracked_objects[class_name] > 5:
                    tracked_objects[class_name] = frame_id  # Update last detected frame
                    print(f"Detected: {class_name} | Estimated Weight: {weight} kg")  # Print to console

                    # Save data to MongoDB Atlas
                    data = {
                        "garbage_type": class_name,
                        "weight_kg": weight,
                        "timestamp": datetime.now()
                    }
                    collection.insert_one(data)  # Insert into MongoDB Atlas

                # Draw bounding box and label
                cvzone.cornerRect(img, (x1, y1, w, h), t=2)
                label = f'{class_name} {conf} | {weight} kg'
                cvzone.putTextRect(img, label, (max(0, x1), max(35, y1)), scale=1, thickness=1)

    # Display the image with detections
    cv2.imshow("Live Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()