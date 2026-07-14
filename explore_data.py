import cv2
import numpy as np

# Use the COLOR mask instead of the grayscale mask - more reliable
color_mask_path = r"data\CholecSeg8k\video01\video01_28900\frame_28900_endo_color_mask.png"

img = cv2.imread(color_mask_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Check if grasper color (170, 255, 0) exists anywhere in this image
grasper_color = np.array([170, 255, 0])
mask_match = np.all(img_rgb == grasper_color, axis=-1)
print("Grasper pixels found:", np.sum(mask_match))

# Check for L-hook color (169, 255, 184)
lhook_color = np.array([169, 255, 184])
mask_match2 = np.all(img_rgb == lhook_color, axis=-1)
print("L-hook pixels found:", np.sum(mask_match2))

# Show all unique colors actually present, so we can sanity-check
unique_colors = np.unique(img_rgb.reshape(-1, 3), axis=0)
print("Number of unique colors:", len(unique_colors))
print(unique_colors)