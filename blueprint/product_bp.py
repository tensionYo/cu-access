# encoding = utf-8
from flask import Blueprint, request
from flask_login import login_required
from utils.decorator import json_resp, admin_role
from blueprint.product_service import *

bp = Blueprint('product_bp', __name__, url_prefix='/product')

DEFAULT_EMPTY = '--EMPTY--'
PRODUCT_KEYS = ['bandwidth', 'delay', 'packet_loss_rate']


@bp.route('/create/')
@login_required
@json_resp
@admin_role
def create_product():
    params = []
    for k in PRODUCT_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    add_product(params)
    return dict(success=True, data='ok')


@bp.route('/save/')
@login_required
@json_resp
@admin_role
def modify_product():
    return None
