# 图像相似度搜索系统

## 项目介绍

这是一个基于深度学习的图像相似度搜索系统，可以帮助用户快速找到与目标图片相似的图像。系统使用预训练的 ResNet50 模型提取图像特征，结合 FAISS 向量索引实现高效的相似图像检索。

### 主要特性

- 使用预训练的 ResNet50 模型进行特征提取
- 支持多种图片格式 (JPG, JPEG, PNG, BMP, GIF)
- 使用 FAISS 进行高效的向量相似度检索
- SQLite 数据库持久化存储特征向量
- Web 界面支持在线图片搜索
- 支持批量导入图片建立索引

## 技术栈

- Python 3.x
- PyTorch (深度学习框架)
- FAISS (向量检索库)
- Flask (Web 框架)
- SQLite (数据库)
- PIL (图像处理)

## 安装部署

### 1. 环境要求

- Python 3.7 或更高版本
- CUDA（可选，用于 GPU 加速）

### 2. 安装依赖

```bash
pip install torch torchvision
pip install faiss-cpu  # 如果使用 GPU，请安装 faiss-gpu
pip install flask
pip install Pillow
```

### 3.项目结构
```plaintext
img_search/  
├── static/          # 静态文件目录  
│   └── images/      # 图片存储目录  
├── templates/       # HTML 模板  
│   └── index.html   # 主页面  
├── utils/          # 工具类  
│   ├── feature_extractor.py  # 特征提取器  
│   ├── image_search.py       # 图像搜索核心  
│   └── database.py          # 数据库操作  
├── app.py          # Flask 应用主文件  
└── test.py         # 测试脚本  
```

## 使用说明

### 1.建立索引
在使用搜索功能前，需要先建立图像索引。
使用测试脚本，或者下面这个代码，将你想要索引的图片都放在 static/images 文件夹下。

```python
from utils.image_search import ImageSearch

image_search = ImageSearch()
image_dir = "static/images"  # 图片目录
image_search.build_index_from_directory(image_dir)
```



### 2.启动项目
1. 运行 app.py 启动 Flask 应用。

```bash
python app.py
```

2. 打开浏览器，访问 2. 打开浏览器，访问 http://127.0.0.1:5000 进入主页面。

3. 上传目标图片，点击搜索按钮，系统将返回与目标图片相似的图像。系统会返回最相似的 5 张图片及其相似度分数

### 3.注意事项

- 确保 static/images 目录存在并有适当的读写权限
- 首次运行时会自动创建 SQLite 数据库文件
- 建议使用 GPU 来加速特征提取过程
- 图片索引建立过程可能较慢，请耐心等待

## 后续优化建议

- 使用 GPU 进行特征提取
- 对于大规模图库，建议使用 FAISS 的 GPU 版本
- 可以通过调整 FAISS 索引类型来平衡查询速度和准确性
