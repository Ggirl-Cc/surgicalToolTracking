from ultralytics import YOLO

model = YOLO("yolov8n.pt")
results = model("https://ultralytics.com/images/bus.jpg")
results[0].show()