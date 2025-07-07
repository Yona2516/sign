import os
import numpy as np

def clean_dataset(root_dir="dataset"):
    removed = 0
    for label_dir in os.listdir(root_dir):
        folder = os.path.join(root_dir, label_dir)
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            try:
                data = np.load(path)
                if data.shape != (30, 225):
                    raise ValueError("Wrong shape")
            except:
                print(f"Removed: {path}")
                os.remove(path)
                removed += 1
    print(f"Cleanup complete: {removed} files removed.")

if __name__ == "__main__":
    clean_dataset()
