import timm
import torch

model = timm.create_model(
    "mobilenetv3_small_100",
    pretrained=True
)

torch.save(model.state_dict(), "mobilenetv3_small.pth")