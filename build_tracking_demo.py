from ultralytics import YOLO

# Using your v2 model - trained on CholecTrack20, 7 classes, proper train/val split
model = YOLO("runs/detect/surgical_tool_v2/weights/best.pt")

video_path = r"data\CholecTrack20\Testing\VID01\Video.mp4"

results = model.track(
    source=video_path,
    tracker="bytetrack.yaml",
    save=True,
    project="runs/track",
    name="demo_v2"
)

print("Done! Check runs/track/demo_v2 for the output video")