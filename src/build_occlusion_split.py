import json
import os
import glob
import shutil

base_dir = r"data\CholecTrack20\Validation"
video_folders = glob.glob(os.path.join(base_dir, "VID*"))

os.makedirs("occlusion_eval/clean/images", exist_ok=True)
os.makedirs("occlusion_eval/clean/labels", exist_ok=True)
os.makedirs("occlusion_eval/hard/images", exist_ok=True)
os.makedirs("occlusion_eval/hard/labels", exist_ok=True)

clean_count = 0
hard_count = 0

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
        frame_filename = f"{int(frame_key):06d}.png"
        frame_path = os.path.join(frames_dir, frame_filename)
        
        if not os.path.exists(frame_path):
            continue
        
        # A frame is "hard" if ANY detection in it flags bleeding, smoke, or occlusion
        is_hard = any(
            det.get("bleeding", 0) == 1 or 
            det.get("smoke", 0) == 1 or 
            det.get("occluded", 0) == 1
            for det in detections
        )
        
        # Build the label lines (same conversion as before)
        lines = []
        for det in detections:
            class_id = det["instrument"]
            x, y, w, h = det["tool_bbox"]
            x_c = x + w / 2
            y_c = y + h / 2
            lines.append(f"{class_id} {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}")
        
        if not lines:
            continue
        
        unique_name = f"{video_name}_{frame_filename}"
        category = "hard" if is_hard else "clean"
        
        shutil.copy(frame_path, f"occlusion_eval/{category}/images/{unique_name}")
        label_name = unique_name.replace(".png", ".txt")
        with open(f"occlusion_eval/{category}/labels/{label_name}", "w") as f:
            f.write("\n".join(lines))
        
        if category == "hard":
            hard_count += 1
        else:
            clean_count += 1

print(f"Clean frames: {clean_count}")
print(f"Hard (occluded/bleeding/smoke) frames: {hard_count}")