# -*- coding: utf-8 -*-
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
    device_ip = request.args.get('DEVICE_IP')
    result = link_relation(device_ip)
    return dict(success=True, data=result)

@bp.route('/Device_interface_matching_south/')
@json_resp
def Device_interface_matching_south():
    olt_ip = request.args.get('OLT_IP')
    print(olt_ip)
    result = device_interface_matching_south(olt_ip)
    return dict(success=True, data=result)



@bp.route('/link_tree/')
@json_resp
def link_tree():
    Broadband_account = request.args.get('Broadband_account')
    olt_id = request.args.get('olt_id')
    result = Link_tree(Broadband_account,olt_id)
    return dict(success=True, data=result)

@bp.route('/PON_device_power/')
@json_resp
def PON_device_power_static():
    result = PON_device_power()
    return dict(success=True, data=result)