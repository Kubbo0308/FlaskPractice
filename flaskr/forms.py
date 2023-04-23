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
    email = StringField('メール： ', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード： ', validators=[DataRequired()])
    submit = SubmitField('ログイン')

# 新規登録用のフォーム
class RegisterForm(FlaskForm):
    username = StringField('名前： ', validators=[DataRequired()])
    email = StringField('メール： ', validators=[DataRequired(), Email('メールアドレスを入力してくだちい')])
    submit = SubmitField('新規登録')

    # メースアドレスが既に登録されているか確認
    def validate_email(self, field):
        if User.select_user_by_email(field.data):
            raise ValidationError('このメールアドレスは既に登録されています')

# パスワード再設定用フォーム
class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'パスワード', validators=[DataRequired(), EqualTo('confirm_password', message='パスワードが一致しません')]
    )
    confirm_password = PasswordField('パスワード確認: ', validators=[DataRequired()])
    submit = SubmitField('パスワードを更新する')
    
    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('パスワードは８文字以上です')