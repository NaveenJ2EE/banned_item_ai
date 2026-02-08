import torch
from torchvision import transforms
from PIL import Image
from src.model import load_model

MODEL_PATH = "models/banned_model.pth"
CLASSES = ["gun", "not_gun"]  # must match train_ds.classes

model = load_model(num_classes=2)
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict(img_path):
    img = Image.open(img_path).convert("RGB")
    x = transform(img).unsqueeze(0)

    with torch.no_grad():
        out = model(x)
        probs = torch.softmax(out, dim=1)

    conf, pred = torch.max(probs, 1)
    return CLASSES[pred.item()], round(conf.item(), 3)

# Test on unseen images
tests = [
    "test_images/gun1.jpg",
    "test_images/phone.jpg"
]

for t in tests:
    print(t, predict(t))