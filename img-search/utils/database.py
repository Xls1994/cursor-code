import sqlite3
import numpy as np
import pickle
from pathlib import Path

class ImageDatabase:
    def __init__(self, db_path='images.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path TEXT UNIQUE NOT NULL,
                    feature_vector BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_image(self, image_path: str, feature_vector: np.ndarray):
        """添加图片路径和特征向量到数据库"""
        serialized_vector = pickle.dumps(feature_vector)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO images (image_path, feature_vector) VALUES (?, ?)',
                (image_path, serialized_vector)
            )
            conn.commit()

    def get_all_features(self):
        """获取所有特征向量和对应的图片路径"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT image_path, feature_vector FROM images')
            rows = cursor.fetchall()
            
            image_paths = []
            features = []
            for row in rows:
                image_paths.append(row[0])
                feature_vector = pickle.loads(row[1])
                features.append(feature_vector)
            
            return image_paths, np.array(features, dtype='float32')

    def delete_image(self, image_path: str):
        """从数据库中删除指定图片"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM images WHERE image_path = ?', (image_path,))
            conn.commit()

    def clear_database(self):
        """清空数据库"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM images')
            conn.commit()