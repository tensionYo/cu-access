# encoding = utf-8
from flask import Blueprint, request
from flask_login import login_required
from utils.decorator import json_resp, admin_role
from task4_service import *


bp = Blueprint('task1_bp4', __name__, url_prefix='/api')

DEFAULT_EMPTY = '--EMPTY--'

@bp.route('/Device_interface_matching/')
@json_resp
def Device_interface_matching_north():
    result = device_interface_matching()
    return dict(success=True, data=result)

@bp.route('/Link_reletion/')
@json_resp
def Link_reletion():
    result = link_relation()
    return dict(success=True, data1=result)

@bp.route('/Device_interface_matching_south/')
@json_resp
def Device_interface_matching_south():
    result = device_interface_matching_south()
    return dict(success=True, data=result)