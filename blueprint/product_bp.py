# encoding = utf-8
from flask import Blueprint, request
from flask_login import login_required
from utils.decorator import json_resp, admin_role
from blueprint.product_service import *

bp = Blueprint('product_bp', __name__, url_prefix='/product')

PRODUCT_KEYS = []


@bp.route('/create/')
@login_required
@json_resp
@admin_role
def create_product():
    params = {}
    for k in PRODUCT_KEYS:
        params[k] = request.args.get(k, '').encode('utf-8')
    add_product(params)
    return dict(success=True, data='ok')


@bp.route('/save/')
@login_required
@json_resp
@admin_role
def modify_product():
    return None
