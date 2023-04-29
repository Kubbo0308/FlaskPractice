from datetime import datetime

from flask import (
    Blueprint, abort, request, render_template,
    redirect, url_for, flash, session, jsonify
)
from flask_login import (
    login_user, login_required, logout_user, current_user
)
from flaskr.models import User, PasswordResetToken
from flaskr import db

from flaskr.forms import (
    LoginForm, RegisterForm, ResetPasswordForm,
    ForgotPasswordForm, UserForm
)

bp = Blueprint('app', __name__, url_prefix='')

# ホーム
@bp.route('/')
def home():
    return render_template('home.html')

# ログアウト時
@bp.route('/logout')
def logout():
    logout_user() # ログアウト
    return redirect(url_for('app.home'))

# ログイン時
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # インスタンス生成
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # メールアドレスが存在するか確認
        user = User.select_user_by_email(form.email.data)
        # ユーザが存在し、アクティブであり、パスワードが正しい場合
        if user and user.is_active and user.validate_password(form.password.data):
            login_user(user, remember=True)
            # ログイン後の移動先
            next = request.args.get('next')
            if not next:
                next = url_for('app.home')
            return redirect(next)
        elif not user:
            flash('存在しないユーザーです')
        elif not user.is_active:
            flash('無効なユーザです。パスワードを再設定してください')
        elif not user.validate_password(form.password.data):
            flash('メールアドレスとパスワードの組み合わせが間違っています')
    return render_template('login.html', form=form)

# 新規登録時
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # インスタンス生成
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # Userクラスのインスタンス生成
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        # dbに追加
        user.create_new_user()
        db.session.commit()
        token = ''
        token = PasswordResetToken.publish_token(user)
        db.session.commit()
        # メールに飛ばすほうがいい
        print(
            f'パスワード設定用URL: http://127.0.0.1:5000/reset_password/{token}'
        )
        flash('パスワード設定用のURLをお送りしました。ご確認ください')
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)

# パスワード設定時
@bp.route('/reset_password/<uuid:token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm(request.form)
    reset_user_id = PasswordResetToken.get_user_id_by_token(token)
    if not reset_user_id:
        abort(500)
    if request.method == 'POST' and form.validate():
        password = form.password.data
        user = User.select_user_by_id(reset_user_id)
        user.save_new_password(password)
        PasswordResetToken.delete_token(token)
        db.session.commit()
        flash('パスワードを更新しました')
        return redirect(url_for('app.login'))
    return render_template('reset_password.html', form=form)

# パスワード忘れた時
@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = User.select_user_by_email(email)
        if user:
            token = PasswordResetToken.publish_token(user)
            db.session.commit()
            reset_url = f'http://127.0.0.1:5000/reset_password/{token}'
            print(reset_url)
            flash('パスワード再登録用のURLを発行しました')
        else:
            flash('存在しないユーザです')
    return render_template('forgot_password.html', form=form)

# ユーザ登録情報変更時
@bp.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        # ユーザ情報をidから取得する為に現在のユーザのidを調べる
        user_id = current_user.get_id()
        user = User.select_user_by_id(user_id)
        user.username = form.username.data
        user.email = form.email.data
        file = request.files[form.picture_path.name].read()
        if file:
            file_name = user_id + '_' + str(int(datetime.now().timestamp())) + 'jpg'
            picture_path = 'flaskr/static/user_image/' + file_name
            open(picture_path, 'wb').write(file)
            user.picture_path = 'user_image/' + file_name
        db.session.commit()
        flash('ユーザ情報の更新に成功しました')
    return render_template('user.html', form=form)