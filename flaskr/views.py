from datetime import datetime

from flask import (
    Blueprint, abort, request, render_template,
    redirect, url_for, flash, session, jsonify
)
from flask_login import (
    login_user, login_required, logout_user, current_user
)
from flaskr.models import User
from flaskr import db

from flaskr.forms import (
    LoginForm, RegisterForm
)

bp = Blueprint('app', __name__, url_prefix='')

# ホーム
@bp.route('/')
def home():
    return render_template('home.html')

# ログアウト時
@bp.route('/logout')
def logout():
    logout_user