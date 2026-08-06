import json
import glob
from collections import Counter

base_dir = r"data\CholecTrack20\Training"
video_folders = glob.glob(f"{base_dir}\\VID*")

class_names = {0: 'grasper', 1: 'bipolar', 2: 'hook', 3: 'scissors', 
               4: 'clipper', 5: 'irrigator', 6: 'specimen-bag'}

counts = Counter()

for video_folder in video_folders:
    import os
    video_name = os.path.basename(video_folder)
    json_path = os.path.join(video_folder, f"{video_name}.json")
    
    with open(json_path, "r") as f:
        data = json.load(f)
    
    for frame_key, detections in data["annotations"].items():
        for det in detections:
            counts[det["instrument"]] += 1

print("Training set instance counts per class:")
for class_id in sorted(counts.keys()):
    print(f"  {class_names[class_id]}: {counts[class_id]}")

total = sum(counts.values())
print(f"\nTotal instances: {total}")
print(f"\nImbalance ratio (most vs least common):")
max_count = max(counts.values())
min_count = min(counts.values())
print(f"  {max_count} / {min_count} = {max_count/min_count:.1f}x")