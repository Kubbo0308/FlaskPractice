from flask_wtf import FlaskForm
from wtforms.form import Form
from wtforms.fields import (
    StringField, FileField, PasswordField, SubmitField, HiddenField, TextAreaField
)
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_login import current_user
from flaskr.models import User
from flask import flash

# ログイン用のフォーム
class LoginForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Email()], render_kw={"placeholder": "例）example@mail.com"})
    password = PasswordField('', validators=[DataRequired()], render_kw={"placeholder": "パスワードを入力"})
    submit = SubmitField('ログイン')

# 新規登録用のフォーム
class RegisterForm(FlaskForm):
    username = StringField('', validators=[DataRequired()], render_kw={"placeholder": "ユーザーネームを入力"})
    email = StringField('', validators=[DataRequired(), Email('メールアドレスを入力してくだちい')], render_kw={"placeholder": "例）example@mail.com"})
    submit = SubmitField('新規登録')

    # メースアドレスが既に登録されているか確認
    def validate_email(self, field):
        if User.select_user_by_email(field.data):
            raise ValidationError('このメールアドレスは既に登録されています')

# パスワード再設定用フォーム
class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        '', validators=[DataRequired(), EqualTo('confirm_password', message='パスワードが一致しません')], render_kw={"placeholder": "パスワードを入力"}
    )
    confirm_password = PasswordField('', validators=[DataRequired()], render_kw={"placeholder": "パスワードを再入力"})
    submit = SubmitField('パスワードを更新する')

    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('パスワードは８文字以上です')

# パスワードを忘れた時用のフォーム
class ForgotPasswordForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Email()], render_kw={"placeholder": "例）example@mail.com"})
    submit = SubmitField('パスワードを再設定する')

    def validate_email(self, field):
        if not User.select_user_by_email(field.data):
            raise ValidationError('そのメールアドレスは存在しません')

# ユーザの情報を変更する用のフォーム
class UserForm(FlaskForm):
    email = StringField('メール： ', validators=[DataRequired(), Email('メールアドレスが間違っています')], render_kw={"placeholder": "例）example@mail.com"})
    username = StringField('名前： ', validators=[DataRequired()], render_kw={"placeholder": "ユーザーネームを入力"})
    picture_path = FileField('')
    submit = SubmitField('登録情報更新')

    def validate(self):
        if not super(FlaskForm, self).validate():
            return False
        user = User.select_user_by_email(self.email.data)
        if user:
            # 現在のユーザとidが等しくない（違うユーザが存在するメールアドレスを登録するのを防ぐ）
            if user.id != int(current_user.get_id()):
                flash('そのメールアドレスは既に登録されています')
                return False
        return True

# パスワードを変更する用のフォーム
class ChangePassword(FlaskForm):
    password = PasswordField('', validators=[DataRequired(), EqualTo('confirm_password', message='パスワードが一致しません')], render_kw={"placeholder": "パスワードを入力"})
    confirm_password = PasswordField('', validators=[DataRequired()], render_kw={"placeholder": "パスワードを再入力"})
    submit = SubmitField('パスワード再設定')

    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('パスワードは８文字以上です')

# ボイスを投稿する用のフォーム
class CreateVoiceForm(FlaskForm):
    title = StringField('', validators=[DataRequired()], render_kw={"placeholder": "タイトルを入力"})
    voice = TextAreaField('', validators=[DataRequired()], render_kw={"placeholder": "本文を入力"})
    picture_path = FileField('', default='')
    submit = SubmitField('ボイス投稿')


# ボイスを更新する用のフォーム
class UpdateVoiceForm(FlaskForm):
    title = StringField('', validators=[DataRequired()])
    voice = TextAreaField('', validators=[DataRequired()])
    picture_path = FileField('', default='')
    submit = SubmitField('ボイス更新')