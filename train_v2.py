from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.train(
    data="data_v2.yaml",
    epochs=10,
    imgsz=416,
    batch=16,
    name="surgical_tool_v2"
)