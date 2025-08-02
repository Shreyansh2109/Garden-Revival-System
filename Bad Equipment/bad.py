import cv2
import math
import cvzone
from ultralytics import YOLO

# Load trained YOLO model
yolo_model = YOLO("Weights/best.pt")

# Read input image
#img = cv2.imread("Media/img2.jpeg") 
img = cv2.imread("Media/img3.webp")  

# Verify image loaded
if img is None:
    print("Image not found. Check file path!")
    exit()

# Perform object detection
results = yolo_model(img)

# Loop through detections
for r in results:
    boxes = r.boxes
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box
        w, h = x2 - x1, y2 - y1  # Calculate width and height

        conf = round(box.conf[0].item(), 2)  # Confidence score

        # Debug: Show detection details
        print(f"Detected: Bad Condition at ({x1}, {y1}) with confidence {conf}")

        # Draw bounding box and label "Bad Condition"
        cvzone.cornerRect(img, (x1, y1, w, h), t=3, rt=5)
        label = f"Bad Condition ({conf})"
        cvzone.putTextRect(img, label, (max(0, x1), max(35, y1)), scale=1, thickness=1)

# Resize and display
img_resized = cv2.resize(img, (800, 600))
cv2.imshow("Bad Equipment Detection", img_resized)

# Close window when 'q' is pressed
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
