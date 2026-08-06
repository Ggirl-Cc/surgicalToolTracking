from ultralytics import YOLO
import json
import os

model = YOLO("runs/detect/surgical_tool_v3/weights/best.pt")

# Find a validation image that actually contains an irrigator (class_id 5)
label_dir = "dataset_v2/val/labels"
irrigator_image = None

for label_file in os.listdir(label_dir):
    with open(os.path.join(label_dir, label_file)) as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith("5 "):  # class_id 5 = irrigator
            irrigator_image = label_file.replace(".txt", ".png")
            break
    if irrigator_image:
        break

print(f"Testing on: {irrigator_image}")
image_path = f"dataset_v2/val/images/{irrigator_image}"

results = model(image_path, conf=0.1)  # lower confidence threshold to see ANY predictions
results[0].save(filename="irrigator_diagnosis.png")

print("\nAll predictions (even low-confidence ones):")
for box in results[0].boxes:
    class_id = int(box.cls[0])
    class_name = model.names[class_id]
    confidence = float(box.conf[0])
    print(f"  {class_name}: {confidence:.2%}")