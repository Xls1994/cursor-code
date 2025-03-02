import faiss
import numpy as np
import os
from .feature_extractor import FeatureExtractor
from .database import ImageDatabase

class ImageSearch:
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.index = None
        self.image_paths = []
        self.db = ImageDatabase()
    
    def build_index(self, image_paths):
        features = []
        for path in image_paths:
            feature = self.feature_extractor.extract(path)
            features.append(feature)
            # 保存到数据库
            self.db.add_image(path, feature)
        
        features = np.array(features).astype('float32')
        self.index = faiss.IndexFlatL2(features.shape[1])
        self.index.add(features)
        self.image_paths = image_paths
    
    def load_index(self):
        """从数据库加载索引"""
        self.image_paths, features = self.db.get_all_features()
        if len(features) > 0:
            self.index = faiss.IndexFlatL2(features.shape[1])
            self.index.add(features)
        
    def build_index_from_directory(self, directory_path):
        """从指定目录读取图片并构建索引"""
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        image_paths = []
        
        # 遍历目录下的所有文件
        for root, _, files in os.walk(directory_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in supported_formats:
                    # 使用绝对路径
                    full_path = os.path.abspath(os.path.join(root, file))
                    image_paths.append(full_path)
        
        if not image_paths:
            raise ValueError(f"在目录 {directory_path} 中没有找到支持的图片文件")
        
        print(f"找到 {len(image_paths)} 个图片文件，开始构建索引...")
        self.build_index(image_paths)
        print("索引构建完成")
        
    def search(self, query_image_path, k=5):
        query_feature = self.feature_extractor.extract(query_image_path)
        query_feature = np.array([query_feature]).astype('float32')
        
        distances, indices = self.index.search(query_feature, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                'image_path': self.image_paths[idx],
                'similarity': float(1 / (1 + distances[0][i]))
            })
        
        return results