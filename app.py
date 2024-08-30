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
        edited_image_path = add_half_black_rectangle(image_path)
        return send_from_directory(save_directory, edited_image_path)

def add_half_black_rectangle(image_path):
    with Image.open(image_path) as image:
        draw = ImageDraw.Draw(image)
        width, height = image.size
        # 画像の中心に小さい四角形を残し、外側を黒塗り
        margin = 0.25  # 内側の四角形のサイズを調整する割合
        inner_x0, inner_y0 = width * margin, height * margin
        inner_x1, inner_y1 = width * (1 - margin), height * (1 - margin)
        
        # 全体を黒塗り
        draw.rectangle([0, 0, width, height], fill='black')
        # 内側の四角形を透明にする
        draw.rectangle([inner_x0, inner_y0, inner_x1, inner_y1], fill=None)
        
        edited_image_path = f"edited_{Path(image_path).name}"
        save_path = os.path.join(save_directory, edited_image_path)
        image.save(save_path)
        return edited_image_path

if __name__ == '__main__':
    app.run(debug=True)