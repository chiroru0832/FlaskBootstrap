from flask import Blueprint, jsonify, request, redirect, url_for, flash, session
from app import db
from models import User
from models import External_data
from models import Validateuser
from services.external_api import fetch_users

api_bp = Blueprint('api', __name__)



@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'email': user.email
    } for user in users])


@api_bp.route('/sync-users', methods=['POST'])
def sync_users():
    try:
        # 外部APIからデータを取得
        users_data = fetch_users()
        if not users_data:
            return jsonify({"error": "Failed to fetch data from external API"}), 500

        # データベースに保存
        for user_data in users_data:
            # 重複チェック
            existing_user = External_data.query.filter_by(email=user_data["email"]).first()
            if not existing_user:
                # 新しいユーザーを追加
                user = External_data(
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    email=user_data["email"],
                    phone=user_data["phone"],
                    city=user_data["city"],
                    state=user_data["state"],
                    country=user_data["country"],
                    profile_picture=user_data["profile_picture"]
                )
                db.session.add(user)
        
        # コミットして保存
        db.session.commit()

        return jsonify({"message": "Users synchronized successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@api_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']

    # ユーザー認証
    user = Validateuser.validate_user(username)
    
    if user:
        # 認証成功
        session['username'] = user.username
        return redirect(url_for('views.home'))  # 'views.home'にリダイレクト
    else:
        # 認証失敗
        return jsonify({"error": "Invalid username"}), 401

@api_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out.', 'info')  # フラッシュメッセージを追加（任意）
    return redirect(url_for('views.login_view'))