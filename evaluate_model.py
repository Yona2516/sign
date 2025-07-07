from dataset_loader import SignDataset
from model.model import SignLanguageLSTM
import torch
from sklearn.metrics import classification_report

dataset = SignDataset()
model = SignLanguageLSTM(input_size=225, hidden_size=128, output_size=len(dataset.label_encoder.classes_))
model.load_state_dict(torch.load("model/lstm_model.pt"))
model.eval()

X, y_true = dataset.data, dataset.labels
with torch.no_grad():
    y_pred = model(X).argmax(dim=1)

print(classification_report(y_true, y_pred, target_names=dataset.label_encoder.classes_))
