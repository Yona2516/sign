import os
import numpy as np

DATASET_DIR = "dataset"
X, y = [], []
labels = sorted(os.listdir(DATASET_DIR))

for idx, label in enumerate(labels):
    folder = os.path.join(DATASET_DIR, label)
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        data = np.load(path)
        if data.shape == (30, 225):
            X.append(data)
            y.append(idx)

X = np.array(X)
y = np.array(y)

np.save("X.npy", X)
np.save("y.npy", y)
print(f"Saved X.npy ({X.shape}) and y.npy ({y.shape})")
