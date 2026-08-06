import os
import glob
import shutil
import random

random.seed(42)  # reproducible split

images = glob.glob("dataset/images/*.png")
random.shuffle(images)

split_idx = int(len(images) * 0.8)  # 80% train, 20% val
train_images = images[:split_idx]
val_images = images[split_idx:]

for folder in ["dataset/train/images", "dataset/train/labels", "dataset/val/images", "dataset/val/labels"]:
    os.makedirs(folder, exist_ok=True)

def move_set(image_list, split_name):
    for img_path in image_list:
        filename = os.path.basename(img_path)
        label_filename = filename.replace(".png", ".txt")
        label_path = os.path.join("dataset/labels", label_filename)
        
        shutil.copy(img_path, f"dataset/{split_name}/images/{filename}")
        if os.path.exists(label_path):
            shutil.copy(label_path, f"dataset/{split_name}/labels/{label_filename}")

move_set(train_images, "train")
move_set(val_images, "val")

print(f"Train: {len(train_images)} images")
print(f"Val: {len(val_images)} images")