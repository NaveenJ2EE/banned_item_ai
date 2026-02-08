import torch
import torch.nn as nn
from torchvision import models


def load_model(num_classes):
    # Load pretrained MobileNetV3
    model = models.mobilenet_v3_large(pretrained=True)

    # Freeze backbone (optional but recommended)
    for param in model.features.parameters():
        param.requires_grad = False

    # Replace classifier (THIS FIXES YOUR ERROR)
    in_features = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(in_features, num_classes)

    return model