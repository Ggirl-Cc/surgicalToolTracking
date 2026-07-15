from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.train(
    data="data.yaml",
    epochs=10,        # fewer epochs
    imgsz=416,         # smaller image size = faster
    batch=16,          # can try larger batch since images are smaller now
    name="surgical_tool_v1"
)