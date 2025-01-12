from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User
from models import External_data
from models import Validateuser

# views用のBlueprint
views_bp = Blueprint('views', __name__)

# ログイン状態をチェック
@views_bp.before_request
def check_login():
    # ログインページはアクセス制限しない
    allowed_routes = ['views.login_view', 'api.login']
    if 'username' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('views.login_view'))

@views_bp.route("/")
def home():
    users = User.query.all()
    external_data = External_data.query.all()
    return render_template('index.html', users=users, external_data=external_data)

@views_bp.route('/upload')
def upload():
    return render_template('upload.html', title="File Uploadページ")

@views_bp.route('/codi')
def codi():
    return render_template('codi.html', title="CoDiページ")

@views_bp.route('/compare')
def compare():
    return render_template('compare.html', title="Compareページ")

@views_bp.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form['username']

        # ユーザー認証
        user = Validateuser.validate_user(username)
        
        if user:
            # 認証成功
            session['username'] = user.username
            return redirect(url_for('views.home'))  # ダッシュボードにリダイレクト
        else:
            # 認証失敗
            flash('Invalid username or password!', 'danger')  # フラッシュメッセージ
            return redirect(url_for('views.login_view'))  # ログインページにリダイレクト

    return render_template('login.html', title="Loginページ")