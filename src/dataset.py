from torchvision import datasets, transforms

def get_datasets(data_dir):
    tfm = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2),
        transforms.ToTensor()
    ])

    train_ds = datasets.ImageFolder(f"{data_dir}/train", transform=tfm)
    val_ds = datasets.ImageFolder(f"{data_dir}/val", transform=tfm)
    return train_ds, val_ds