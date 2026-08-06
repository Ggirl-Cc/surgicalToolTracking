from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.train(
    data="data_v2.yaml",
    epochs=10,
    imgsz=640,  # increased from 416 -> targets small object detection
    batch=8,    # reduced batch since larger images use more memory
    name="surgical_tool_v3"
)