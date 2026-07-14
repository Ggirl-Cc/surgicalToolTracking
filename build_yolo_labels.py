import cv2
import numpy as np
import os
import glob
import shutil

def get_bounding_box(mask_path, target_color, tolerance=10):
    img = cv2.imread(mask_path)
    if img is None:
        return None
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    target = np.array(target_color)
    diff = np.abs(img_rgb.astype(int) - target.astype(int))
    match = np.all(diff <= tolerance, axis=-1)
    if np.sum(match) == 0:
        return None
    ys, xs = np.where(match)
    return (xs.min(), ys.min(), xs.max(), ys.max())

def to_yolo_format(box, img_width, img_height, class_id):
    x_min, y_min, x_max, y_max = box
    x_center = (x_min + x_max) / 2 / img_width
    y_center = (y_min + y_max) / 2 / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height
    return f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"

# Class IDs: 0 = grasper, 1 = lhook
GRASPER_COLOR = [170, 255, 0]
LHOOK_COLOR = [169, 255, 184]

folder = r"data\CholecSeg8k\video01\video01_28900"

# Output folders - this is the structure YOLO expects
os.makedirs("dataset/images", exist_ok=True)
os.makedirs("dataset/labels", exist_ok=True)

mask_files = glob.glob(os.path.join(folder, "*_color_mask.png"))

processed = 0
for mask_path in mask_files:
    filename = os.path.basename(mask_path)
    frame_id = filename.replace("_color_mask.png", "")
    
    raw_img_path = os.path.join(folder, frame_id + ".png")
    if not os.path.exists(raw_img_path):
        continue
    
    img = cv2.imread(raw_img_path)
    h, w = img.shape[:2]
    
    grasper_box = get_bounding_box(mask_path, GRASPER_COLOR)
    lhook_box = get_bounding_box(mask_path, LHOOK_COLOR)
    
    lines = []
    if grasper_box:
        lines.append(to_yolo_format(grasper_box, w, h, 0))
    if lhook_box:
        lines.append(to_yolo_format(lhook_box, w, h, 1))
    
    if not lines:
        continue  # skip frames with no tools at all
    
    # Copy the raw image
    shutil.copy(raw_img_path, f"dataset/images/{frame_id}.png")
    
    # Write the label file
    with open(f"dataset/labels/{frame_id}.txt", "w") as f:
        f.write("\n".join(lines))
    
    processed += 1

print(f"Processed {processed} frames with labels")