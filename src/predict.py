import torch
from PIL import Image
from torchvision import transforms
from model import load_model
import os

# ========== CONFIG ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Define the absolute path to the model
MODEL_PATH = os.path.join(BASE_DIR, "models", "banned_model.pth")
# Put any image path here to test
IMAGE_TO_TEST = "C:/Users/navee/Documents/banned_item_ai/test_images/phone.jpg"
CLASS_NAMES = ["gun", "not_gun"] # Ensure this matches your folder order

device = "cuda" if torch.cuda.is_available() else "cpu"

def predict(img_path):
    # 1. Load Model
    # len(CLASS_NAMES) is 2
    model = load_model(num_classes=len(CLASS_NAMES))
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()

    # 2. Preprocess Image
    tfm = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    image = Image.open(img_path).convert("RGB")
    img_tensor = tfm(image).unsqueeze(0).to(device) # Add batch dimension

    # 3. Inference
    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        confidence, predicted_idx = torch.max(probabilities, 0)

    result = CLASS_NAMES[predicted_idx]
    print(f"\n[!] Prediction: {result.upper()}")
    print(f"[!] Confidence: {confidence.item()*100:.2f}%")

if __name__ == "__main__":
    if os.path.exists(IMAGE_TO_TEST):
        predict(IMAGE_TO_TEST)
    else:
        print(f"[x] File {IMAGE_TO_TEST} not found. Add an image to test!")