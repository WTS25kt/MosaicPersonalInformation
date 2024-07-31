import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_from_directory
from PIL import Image, ImageDraw, ImageFont

# .envファイルを読み込む
load_dotenv()

# 環境変数からパスを取得
font_path = os.getenv('FONT_PATH')
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
        edited_image_path = add_black_rectangle(image_path)
        return send_from_directory(save_directory, edited_image_path)

def add_black_rectangle(image_path):
    with Image.open(image_path) as image:
        draw = ImageDraw.Draw(image)
        # 黒塗りの四角を追加（位置とサイズは適宜調整）
        rectangle_x0, rectangle_y0 = 50, 50
        rectangle_x1, rectangle_y1 = 200, 200
        draw.rectangle([rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1], fill="black")
        edited_image_path = f"edited_{Path(image_path).name}"
        save_path = os.path.join(save_directory, edited_image_path)
        image.save(save_path)
        return edited_image_path

if __name__ == '__main__':
    app.run(debug=True)