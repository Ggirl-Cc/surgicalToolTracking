import json
import glob
import os
from collections import defaultdict

base_dir = r"data\CholecTrack20\Training"
video_folders = glob.glob(f"{base_dir}\\VID*")

class_names = {0: 'grasper', 1: 'bipolar', 2: 'hook', 3: 'scissors', 
               4: 'clipper', 5: 'irrigator', 6: 'specimen-bag'}

sizes = defaultdict(list)

for video_folder in video_folders:
    video_name = os.path.basename(video_folder)
    json_path = os.path.join(video_folder, f"{video_name}.json")
    
    with open(json_path, "r") as f:
        data = json.load(f)
    
    for frame_key, detections in data["annotations"].items():
        for det in detections:
            class_id = det["instrument"]
            w, h = det["tool_bbox"][2], det["tool_bbox"][3]
            area = w * h
            sizes[class_id].append(area)

print("Average bounding box area (normalized, 0-1 scale) per class:")
for class_id in sorted(sizes.keys()):
    avg_area = sum(sizes[class_id]) / len(sizes[class_id])
    print(f"  {class_names[class_id]}: {avg_area:.4f} (n={len(sizes[class_id])})")