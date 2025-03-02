import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from utils.image_search import ImageSearch
# 初始化搜索器
image_search = ImageSearch()

# 构建索引
image_dir = "./static/images"
image_search.build_index_from_directory(image_dir)

# # 加载索引
# image_search.load_index()
# # 之后就可以进行搜索了
# results = image_search.search("./static/1.png")
# print("搜索结果:", results)
