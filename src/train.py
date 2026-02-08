import os

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from model import load_model
from dataset import get_datasets

device = "cuda" if torch.cuda.is_available() else "cpu"

train_ds, val_ds = get_datasets("data")
train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)

model = load_model(num_classes=len(train_ds.classes))
model.to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.classifier.parameters(), lr=0.001)

for epoch in range(5):
    model.train()
    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        out = model(imgs)
        loss = loss_fn(out, labels)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1} done")

# Use absolute path logic to ensure it saves to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_PATH = os.path.join(BASE_DIR, "models", "banned_model.pth")

# Ensure the directory exists
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

torch.save(model.state_dict(), SAVE_PATH)
print(f"[✓] Model saved successfully at: {SAVE_PATH}")
