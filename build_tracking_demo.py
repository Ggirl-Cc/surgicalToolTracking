from ultralytics import YOLO

# Using your v2 model - trained on CholecTrack20, 7 classes, proper train/val split
model = YOLO("runs/detect/surgical_tool_v2/weights/best.pt")

video_path = r"data\CholecTrack20\Testing\VID01\vid01.mp4"

results = model.track(
    source=video_path,
    tracker="bytetrack.yaml",
    save=True,
    project="runs/track",
    name="demo_v2_test",
    vid_stride=5  # only process every 5th frame for faster test run
)

print("Done! Check runs/track/demo_v2 for the output video")