from ultralytics import YOLO
import glob
import random

# Load your trained model - not the generic pretrained one, YOUR trained weights
model = YOLO("runs/detect/surgical_tool_v1-2/weights/best.pt")

# Grab a random image from your validation set to test on
val_images = glob.glob("dataset/val/images/*.png")
test_image = random.choice(val_images)

print(f"Testing on: {test_image}")

# Run detection
results = model(test_image)

# Save the annotated result
results[0].save(filename="my_second_detection.png")

print("Saved as my_second_detection.png - go open it!")

# Also print what it found
for box in results[0].boxes:
    class_id = int(box.cls[0])
    class_name = model.names[class_id]
    confidence = float(box.conf[0])
    print(f"Detected: {class_name} (confidence: {confidence:.2%})")