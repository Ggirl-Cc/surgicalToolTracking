import json

json_path = r"data\CholecTrack20\Training\VID02\VID02.json"

with open(json_path, "r") as f:
    data = json.load(f)

print("Type of annotations:", type(data["annotations"]))

# If it's a dict, show us the keys
if isinstance(data["annotations"], dict):
    keys = list(data["annotations"].keys())
    print("Number of keys:", len(keys))
    print("First 5 keys:", keys[:5])
    
    # Show the value for the first key
    first_key = keys[0]
    print(f"\nValue for key '{first_key}':")
    print(json.dumps(data["annotations"][first_key], indent=2)[:1000])