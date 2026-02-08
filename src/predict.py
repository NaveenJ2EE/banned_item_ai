import torch
from PIL import Image
from torchvision import transforms
from model import load_model
from ocr import extract_text

labels = ["weapon", "alcohol", "adult", "allowed"]

def predict(image_path):
    model = load_model(len(labels))
    model.load_state_dict(torch.load("models/banned_model.pth", map_location="cpu"))
    model.eval()

    tfm = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor()
    ])

    img = Image.open(image_path).convert("RGB")
    img = tfm(img).unsqueeze(0)

    with torch.no_grad():
        out = model(img)
        prob = torch.softmax(out, dim=1)
        conf, idx = torch.max(prob, 1)

    text = extract_text(image_path)

    return labels[idx], conf.item(), text