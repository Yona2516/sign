import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from dataset_loader import SignDataset
from model.model import SignLanguageLSTM

dataset = SignDataset()
loader = DataLoader(dataset, batch_size=16, shuffle=True)

model = SignLanguageLSTM(input_size=225, hidden_size=128, output_size=len(dataset.label_encoder.classes_))
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(20):
    total_loss = 0
    for X, y in loader:
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

torch.save(model.state_dict(), "model/lstm_model.pt")
