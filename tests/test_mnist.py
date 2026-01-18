import pytest
from pathlib import Path
import sys

# プロジェクトルートをパスに追加してmnist.pyをインポート可能にする
sys.path.append(str(Path(__file__).parent.parent))

from mnist import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # テスト用アップロードフォルダの設定（必要に応じて）
    # app.config['UPLOAD_FOLDER'] = ...
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """トップページへのアクセス確認"""
    response = client.get('/')
    assert response.status_code == 200
    # レスポンスにタイトルが含まれているか確認
    assert b"AI Number Classifier" in response.data

def test_config_loading(client):
    """設定が正しくロードされているか確認"""
    assert 'UPLOAD_FOLDER' in app.config
    assert 'ALLOWED_EXTENSIONS' in app.config

def test_model_loaded():
    """モデルファイルの読み込み状態を確認"""
    # mnist.pyのグローバルスコープでロードを試みているため、
    # 成功していれば print文が出るが、ここでは変数を直接チェックできない（import時に実行されるため）。
    # インポートされたモジュール内の変数をチェック
    from mnist import model
    # model.h5が存在すればロードされているはず
    if Path('model.h5').exists():
        assert model is not None
    else:
        # モデルがない環境ではNoneであることを許容するか、あるいは失敗とするか
        print("Model file not found, skipping model check.")
