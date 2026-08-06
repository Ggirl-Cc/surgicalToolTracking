import cv2
import numpy as np

def get_bounding_box(mask_path, target_color, tolerance=10):
    """
    Find the bounding box of a specific colored region in a mask image.
    Returns (x_min, y_min, x_max, y_max) or None if not found.
    """
    img = cv2.imread(mask_path)
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

# Test it on our known frame
mask_path = r"data\CholecSeg8k\video01\video01_28900\frame_28900_endo_color_mask.png"

grasper_box = get_bounding_box(mask_path, [170, 255, 0])
lhook_box = get_bounding_box(mask_path, [169, 255, 184])

print("Grasper box:", grasper_box)
print("L-hook box:", lhook_box)