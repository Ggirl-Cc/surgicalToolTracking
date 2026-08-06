from ultralytics import YOLO

model = YOLO("runs/detect/surgical_tool_v3/weights/best.pt")

# Try a few different test videos for variety
test_videos = [
    r"data\CholecTrack20\Testing\VID06\vid06.mp4",
    r"data\CholecTrack20\Testing\VID12\vid12.mp4",
]

for video_path in test_videos:
    video_name = video_path.split("\\")[-1].replace(".mp4", "")
    print(f"\nProcessing {video_name}...")
    
    results = model.track(
        source=video_path,
        tracker="bytetrack.yaml",
        save=True,
        project="runs/track",
        name=f"demo_{video_name}",
        vid_stride=5  # faster test pass, same as before
    )
    print(f"Done with {video_name}")

print("\nAll demos complete!")
