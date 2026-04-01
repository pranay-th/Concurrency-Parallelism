import os
from utils.config import OUTPUT_DIR
import json

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR,exist_ok=True)

def save_json(filename, data):
    ensure_output_dir()
    file_path=os.path.join(OUTPUT_DIR,filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

