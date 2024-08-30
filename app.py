import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_from_directory
from PIL import Image, ImageDraw

# .envファイルを読み込む
load_dotenv()

# 環境変数からパスを取得
save_directory = os.getenv('SAVE_DIRECTORY')

# Flaskアプリケーションの設定
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    image_file = request.files['image']
    if image_file:
        image_path = os.path.join(save_directory, image_file.filename)
        image_file.save(image_path)
        edited_image_path = add_black_borders(image_path)
        return send_from_directory(save_directory, edited_image_path)

def add_black_borders(image_path):
    with Image.open(image_path) as image:
        draw = ImageDraw.Draw(image)
        width, height = image.size
        # 中央に残す四角形のサイズを設定
        margin = 0.25  # 内側の四角形のサイズを調整する割合
        inner_x0, inner_y0 = width * margin, height * margin
        inner_x1, inner_y1 = width * (1 - margin), height * (1 - margin)
        
        # 上部の黒塗り
        draw.rectangle([0, 0, width, inner_y0], fill='black')
        # 下部の黒塗り
        draw.rectangle([0, inner_y1, width, height], fill='black')
        # 左側の黒塗り
        draw.rectangle([0, inner_y0, inner_x0, inner_y1], fill='black')
        # 右側の黒塗り
        draw.rectangle([inner_x1, inner_y0, width, inner_y1], fill='black')
        
        edited_image_path = f"edited_{Path(image_path).name}"
        save_path = os.path.join(save_directory, edited_image_path)
        image.save(save_path)
        return edited_image_path

if __name__ == '__main__':
    app.run(debug=True)