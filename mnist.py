import os
from pathlib import Path
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# プロジェクトのルートディレクトリ設定
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """アプリケーション設定クラス"""
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MODEL_PATH = BASE_DIR / 'model.h5'
    IMAGE_SIZE = 28
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key') # セキュリティのためキーを設定（本番では環境変数推奨）

    # アップロードフォルダが存在しない場合は作成
    UPLOAD_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)
app.config.from_object(Config)

# MNISTのクラスラベル
CLASSES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# モデルの読み込み
try:
    model = load_model(str(app.config['MODEL_PATH']))
    print("モデルの読み込みに成功しました。")
except Exception as e:
    print(f"モデルの読み込みに失敗しました: {e}")
    model = None

def allowed_file(filename: str) -> bool:
    """
    ファイル名が許可された拡張子を持っているか確認します。
    
    Args:
        filename (str): チェックするファイル名
        
    Returns:
        bool: 許可されている場合はTrue
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    メインページ兼ファイルアップロード処理
    GET: アップロードフォームを表示
    POST: 画像を受け取り、推論結果を表示
    """
    if request.method == 'POST':
        # ファイルパートがない場合
        if 'file' not in request.files:
            flash('ファイルがありません', 'error')
            return redirect(request.url)
            
        file = request.files['file']
        
        # ファイル名が空の場合
        if file.filename == '':
            flash('ファイルが選択されていません', 'error')
            return redirect(request.url)
            
        # ファイルがあり、拡張子が許可されている場合
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = app.config['UPLOAD_FOLDER'] / filename
            file.save(upload_path)
            
            # モデルがロードされていない場合のエラーハンドリング
            if model is None:
                flash('モデルが読み込まれていないため、予測できません。', 'error')
                return render_template("index.html", answer="エラー発生")

            try:
                # 画像の読み込みと前処理
                # grayscale=True は非推奨のため color_mode='grayscale' に変更
                img = image.load_img(
                    upload_path, 
                    color_mode='grayscale', 
                    target_size=(app.config['IMAGE_SIZE'], app.config['IMAGE_SIZE'])
                )
                
                # 画像を配列に変換
                img_array = image.img_to_array(img)
                # バッチ次元を追加 (1, 28, 28, 1)
                data = np.array([img_array])
                
                # 推論実行
                result = model.predict(data)[0]
                predicted_idx = result.argmax()
                
                # クラスラベル取得
                pred_label = CLASSES[predicted_idx]
                pred_answer = f"これは {pred_label} です"
                
                return render_template("index.html", answer=pred_answer)
                
            except Exception as e:
                print(f"推論エラー: {e}")
                flash('画像の処理中にエラーが発生しました。', 'error')
                return redirect(request.url)

    return render_template("index.html", answer="")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    # ローカル開発用
    app.run(host='0.0.0.0', port=port, debug=True)