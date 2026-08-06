import json
import os
import glob
import shutil
import time

def tlwh_to_yolo(bbox):
    x, y, w, h = bbox
    x_center = x + w / 2
    y_center = y + h / 2
    return x_center, y_center, w, h

def process_split(split_name):
    base_dir = rf"data\CholecTrack20\{split_name}"
    video_folders = sorted(glob.glob(os.path.join(base_dir, "VID*")))
    
    out_folder = "train" if split_name == "Training" else "val"
    os.makedirs(f"dataset_v2/{out_folder}/images", exist_ok=True)
    os.makedirs(f"dataset_v2/{out_folder}/labels", exist_ok=True)
    
    print(f"\n=== {split_name}: {len(video_folders)} videos ===")
    
    total_processed = 0
    total_skipped = 0
    
    for video_idx, video_folder in enumerate(video_folders, 1):
        video_name = os.path.basename(video_folder)
        json_path = os.path.join(video_folder, f"{video_name}.json")
        
        print(f"[{video_idx}/{len(video_folders)}] {video_name}...")
        
        if not os.path.exists(json_path):
            continue
        
        with open(json_path, "r") as f:
            data = json.load(f)
        
        annotations = data["annotations"]
        frames_dir = os.path.join(video_folder, "Frames")
        
        for frame_key, detections in annotations.items():
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
            shutil.copy(frame_path, f"dataset_v2/{out_folder}/images/{unique_name}")
            
            label_name = unique_name.replace(".png", ".txt")
            with open(f"dataset_v2/{out_folder}/labels/{label_name}", "w") as f:
                f.write("\n".join(lines))
            
            total_processed += 1
    
    print(f"{split_name} done: {total_processed} processed, {total_skipped} skipped")
    return total_processed

train_count = process_split("Training")
val_count = process_split("Validation")

print(f"\n=== FINAL ===")
print(f"Train: {train_count}")
print(f"Val: {val_count}")