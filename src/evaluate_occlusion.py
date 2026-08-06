from ultralytics import YOLO

model = YOLO("runs/detect/surgical_tool_v3/weights/best.pt")

print("=== CLEAN FRAMES ===")
clean_results = model.val(data="data_clean.yaml", split="val")

print("\n=== HARD (OCCLUDED/BLEEDING/SMOKE) FRAMES ===")
hard_results = model.val(data="data_hard.yaml", split="val")