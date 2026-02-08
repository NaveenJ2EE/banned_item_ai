import torch
from PIL import Image
from torchvision import transforms
from model import load_model
from ocr import extract_text

# MUST match train_ds.classes
LABELS = ["gun", "not_gun"]

# Load model ONCE
model = load_model(num_classes=len(LABELS))
model.load_state_dict(torch.load("models/banned_model.pth", map_location="cpu"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict(image_path):
    img = Image.open(image_path).convert("RGB")
    img = transform(img).unsqueeze(0)

    with torch.no_grad():
        out = model(img)
        probs = torch.softmax(out, dim=1)
        conf, idx = torch.max(probs, 1)

    text = extract_text(image_path)

    return LABELS[idx.item()], round(conf.item(), 3), text