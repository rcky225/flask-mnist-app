# Flask MNIST App

このプロジェクトは、手書き数字（0-9）を識別するAIアプリケーションです。
Flaskをバックエンドに、TensorFlow (Keras) を推論エンジンとして使用しています。デザインにはGlassmorphism（すりガラス効果）を取り入れたモダンなUIを採用しています。

## ✨ 主な機能

- **高精度な数字識別**: 事前学習済みのKerasモデルを使用して手書き数字を判定します。
- **モダンなUI**: Glassmorphismデザインと鮮やかなグラデーションアニメーションを採用。
- **直感的な操作**: ドラッグ＆ドロップによる画像アップロードと、クライアントサイドでのプレビュー機能。
- **レスポンシブ対応**: スマートフォンやタブレットでも快適に使用できます。

## 🚀 環境構築と実行

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd flask-mnist-app
```

### 2. 重要: モデルファイルの準備

プロジェクトルートに `model.h5`（学習済みモデル）が必要です。

### 3. 仮想環境の作成（推奨）

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```

### 4. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 5. アプリケーションの起動

```bash
python mnist.py
```

起動後、ブラウザで `http://localhost:8080` にアクセスしてください。

## 🧪 テストの実行

`pytest` を使用してテストを実行できます。

```bash
# テスト用依存関係を含む（requirements.txtに含まれています）
pip install -r requirements.txt

# テスト実行
pytest tests/
```

## 📂 プロジェクト構成

```text
flask-mnist-app/
├── mnist.py                # アプリケーションのエントリーポイント
├── model.h5                # 学習済みモデルファイル（バイナリ）
├── requirements.txt        # 依存ライブラリ一覧
├── static/
│   └── stylesheet.css      # スタイルシート（Glassmorphismデザイン）
├── templates/
│   └── index.html          # HTMLテンプレート
├── tests/                  # テストコードディレクトリ
│   └── test_mnist.py       # 単体テスト
└── uploads/                # アップロードされた画像（自動生成）
```

## 🛠️ 技術スタック

- **Backend**: Python 3, Flask, Werkzeug
- **AI/ML**: TensorFlow (Keras), NumPy, Pillow
- **Frontend**: HTML5, CSS3 (Variables, Flexbox/Grid), JavaScript (Vanilla)
