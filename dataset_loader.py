import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

class CycloneDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        self.data_frame = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        img_path = self.data_frame.iloc[idx]['file_path']
        image = Image.open(img_path).convert('RGB')
        label = int(self.data_frame.iloc[idx]['imd_class'])

        if self.transform:
            image = self.transform(image)

        return image, label

data_transforms = {
    'train': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

if __name__ == '__main__':
    dataset = CycloneDataset('./cyclone_dataset/processed_cyclone_metadata.csv', transform=data_transforms['train'])
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    images, labels = next(iter(dataloader))
    print("Batch image tensor shape:", images.shape)
    print("Batch label tensor shape:", labels.shape) 
    print("Sample labels in batch:", labels.tolist())