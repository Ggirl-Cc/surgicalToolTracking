import json
import os
import glob
import shutil

# Category ID stays the same as CholecTrack20's own numbering (0-6)
# 0=grasper, 1=bipolar, 2=hook, 3=scissors, 4=clipper, 5=irrigator, 6=specimen-bag

def tlwh_to_yolo(bbox):
    """Convert [top_left_x, top_left_y, width, height] (normalized) to YOLO center format"""
    x, y, w, h = bbox
    x_center = x + w / 2
    y_center = y + h / 2
    return x_center, y_center, w, h

base_dir = r"data\CholecTrack20\Training"
video_folders = glob.glob(os.path.join(base_dir, "VID*"))

os.makedirs("dataset_v2/images", exist_ok=True)
os.makedirs("dataset_v2/labels", exist_ok=True)

total_processed = 0
total_skipped = 0

for video_folder in video_folders:
    video_name = os.path.basename(video_folder)
    json_path = os.path.join(video_folder, f"{video_name}.json")
    
    if not os.path.exists(json_path):
        continue
    
    with open(json_path, "r") as f:
        data = json.load(f)
    
    annotations = data["annotations"]
    frames_dir = os.path.join(video_folder, "Frames")
    
    for frame_key, detections in annotations.items():
        # Frame filenames are zero-padded to 6 digits, e.g. "6701" -> "006701.png"
        frame_filename = f"{int(frame_key):06d}.png"
        frame_path = os.path.join(frames_dir, frame_filename)
        
        if not os.path.exists(frame_path):
            total_skipped += 1
            continue
        
        lines = []
        for det in detections:
            class_id = det["instrument"]
            bbox = det["tool_bbox"]
            x_c, y_c, w, h = tlwh_to_yolo(bbox)
            lines.append(f"{class_id} {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}")
        
        if not lines:
            total_skipped += 1
            continue
        
        unique_name = f"{video_name}_{frame_filename}"
        shutil.copy(frame_path, f"dataset_v2/images/{unique_name}")
        
        label_name = unique_name.replace(".png", ".txt")
        with open(f"dataset_v2/labels/{label_name}", "w") as f:
            f.write("\n".join(lines))
        
        total_processed += 1

print(f"Total frames processed: {total_processed}")
print(f"Total frames skipped: {total_skipped}")