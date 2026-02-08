import os
from torchvision import datasets, transforms


def get_datasets(data_dir_name="data"):
    # Calculate absolute path to the project root
    # This assumes dataset.py is in 'src' folder
    current_file_path = os.path.abspath(__file__)  # path to src/dataset.py
    project_root = os.path.dirname(os.path.dirname(current_file_path))
    data_path = os.path.join(project_root, data_dir_name)

    print(f"[*] Looking for data in: {data_path}")

    # Standard ImageNet normalization for MobileNetV3
    stats = ([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

    train_tfm = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(*stats)
    ])

    val_tfm = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(*stats)
    ])

    # Join paths correctly for Windows
    train_path = os.path.join(data_path, "train")
    val_path = os.path.join(data_path, "val")

    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Directory not found: {train_path}. Did you run the splitter?")

    train_ds = datasets.ImageFolder(train_path, transform=train_tfm)
    val_ds = datasets.ImageFolder(val_path, transform=val_tfm)

    return train_ds, val_ds