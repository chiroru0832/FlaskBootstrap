from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# dbインスタンスをアプリケーションの外で作成
db = SQLAlchemy()

def create_app():
    # Flaskアプリケーションを作成
    app = Flask(__name__)

    # 設定ファイルを読み込む
    app.config.from_object(Config)

    # セッション用の秘密鍵を設定
    app.secret_key = 'your_secret_key_here'

    # dbをアプリケーションに関連付ける
    db.init_app(app)

    # ブループリントをアプリケーションに登録
    from routes.views import views_bp  # views用ブループリント
    from routes.api import api_bp      # API用ブループリント
    app.register_blueprint(views_bp, url_prefix='/')  # views用ブループリント
    app.register_blueprint(api_bp, url_prefix='/apiconf')  # API用ブループリント
        

    return app
