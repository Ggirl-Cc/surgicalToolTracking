import cv2
import numpy as np
import os
import glob

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
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
    
    return (x_min, y_min, x_max, y_max)

# Colors for our two tool classes
GRASPER_COLOR = [170, 255, 0]
LHOOK_COLOR = [169, 255, 184]

# Folder to process
folder = r"data\CholecSeg8k\video01\video01_28900"

# Find all color_mask files in this folder
mask_files = glob.glob(os.path.join(folder, "*_color_mask.png"))

print(f"Found {len(mask_files)} color mask files")

results = []

for mask_path in mask_files:
    grasper_box = get_bounding_box(mask_path, GRASPER_COLOR)
    lhook_box = get_bounding_box(mask_path, LHOOK_COLOR)
    
    filename = os.path.basename(mask_path)
    results.append({
        "file": filename,
        "grasper": grasper_box,
        "lhook": lhook_box
    })

# Summary
grasper_count = sum(1 for r in results if r["grasper"] is not None)
lhook_count = sum(1 for r in results if r["lhook"] is not None)

print(f"Frames with grasper detected: {grasper_count}")
print(f"Frames with L-hook detected: {lhook_count}")

# Show a few examples
print("\nFirst 5 results:")
for r in results[:5]:
    print(r)
