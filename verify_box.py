import cv2

# Load the RAW image (not the mask) to draw on
raw_path = r"data\CholecSeg8k\video01\video01_28900\frame_28900_endo.png"
img = cv2.imread(raw_path)

# The box we just found
x_min, y_min, x_max, y_max = 519, 80, 792, 231

# Draw a rectangle around it
cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)

# Save it so we can view it
cv2.imwrite("verification_check.png", img)
print("Saved verification_check.png - open it to check the box")