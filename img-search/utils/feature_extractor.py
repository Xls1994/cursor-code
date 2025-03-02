import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

class FeatureExtractor:
    def __init__(self):
        # 使用预训练的 ResNet50
        self.model = models.resnet50(pretrained=True)
        self.model.eval()
        # 移除最后的全连接层
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])
        
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
    
    def extract(self, image_path):
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image)
        image = image.unsqueeze(0)
        
        with torch.no_grad():
            feature = self.model(image)
        
        return feature.squeeze().numpy()