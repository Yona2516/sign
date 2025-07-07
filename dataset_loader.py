import os
import numpy as np
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import LabelEncoder

class SignDataset(Dataset):
    def __init__(self, dataset_path="dataset"):
        self.data = []
        self.labels = []
        self.label_encoder = LabelEncoder()
        label_names = sorted(os.listdir(dataset_path))
        self.label_encoder.fit(label_names)

        for label in label_names:
            label_folder = os.path.join(dataset_path, label)
            for file in os.listdir(label_folder):
                path = os.path.join(label_folder, file)
                try:
                    data = np.load(path)
                    if data.shape == (30, 225):
                        self.data.append(data)
                        self.labels.append(label)
                except:
                    pass

        self.data = torch.tensor(np.array(self.data), dtype=torch.float32)
        self.labels = torch.tensor(self.label_encoder.transform(self.labels), dtype=torch.long)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]
