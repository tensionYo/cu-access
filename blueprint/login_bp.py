# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect
from utils.decorator import json_resp
from auth.login import get_user
from flask_login import login_user, login_required, logout_user

bp = Blueprint('login_bp', __name__, url_prefix='/auth')


@bp.route('/login/')
@json_resp
def login():
    login_name = request.args.get('login_name', '').encode('utf-8')
    password = request.args.get('password', '').encode('utf-8')
    user = get_user(login_name, password)
    if not user or not user.is_authenticated:
        return dict(success=False, msg='login failed!')

    login_user(user)
    return dict(success=True, data='login done.')


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/auth/login/')
