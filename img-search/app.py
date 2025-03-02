from flask import Flask, request, render_template, jsonify, url_for
from utils.feature_extractor import FeatureExtractor
from utils.image_search import ImageSearch
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

feature_extractor = FeatureExtractor()
image_search = ImageSearch()
image_search.load_index()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return jsonify({'error': '没有上传图片'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '未选择图片'})
    
    # 保存上传的图片
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    
    # 提取特征并搜索
    results = image_search.search(filename, k=5)
    
    # 转换图片路径为URL
    for result in results:
        image_path = result['image_path']
        # 获取相对于static目录的路径
        relative_path = os.path.relpath(image_path, 'static')
        # 将反斜杠转换为正斜杠
        relative_path = relative_path.replace('\\', '/')
        # 转换为URL
        result['image_path'] = url_for('static', filename=relative_path)
    
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)