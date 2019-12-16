# -*- coding: utf-8 -*-
from flask import Blueprint, request
from flask_login import login_required
from utils.decorator import json_resp, admin_role
from blueprint.task5_service import *

bp = Blueprint('task1_bp5', __name__, url_prefix='/api')

DEFAULT_EMPTY = '--EMPTY--'
meal_threshold_KEYS = ['meal_type','down_direction__down_limit','down_direction__up_limit','up_direction_down_limit','up_direction_up_limit']
device_threshold_KEYS = ['device_type','port_type','port_num','user_num_up_boundary','split_user_up_limit']
port_threshold_KEYS = ['device_type','port_type','port_level','down_direction_warn_up_limit','up_direction_warn_up_limit','down_direction_start_up_limit','up_direction_start_up_limit','user_num_up_boundray','FTTB_split_user_num_up_boundary']

@bp.route('/show_meal_threshold/')
@json_resp
def show_meal_thresholdset():
    result =  show_meal_thresholdset_table()
    return dict(success=True, data=result)

@bp.route('/show_device_threshold/')
@json_resp
def show_device_thresholdset():
    result = show_device_thresholdset_table()
    return dict(success=True, data=result)

@bp.route('/show_port_threshold/')
@json_resp
def show_port_thresholdset():
    result = show_port_thresholdset_table()
    return dict(success=True, data=result)

@bp.route('/update_meal_threshold/')
@login_required
@json_resp
@admin_role
def update_meal_threshold():
    params = []
    for k in meal_threshold_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    params.append(request.args.get('id').encode('utf-8'))
    update_meal_threshold_table(params)
    result = show_meal_thresholdset_table()
    return dict(success=True, data=result)


@bp.route('/update_device_threshold/')
@login_required
@json_resp
@admin_role
def update_device_threshold():
    params = []
    for k in device_threshold_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    params.append(request.args.get('id').encode('utf-8'))
    update_device_threshold_table(params)
    result = show_device_thresholdset_table()
    return dict(success=True, data=result)


@bp.route('/update_port_threshold/')
@login_required
@json_resp
@admin_role
def update_port_threshold():
    params = []
    for k in port_threshold_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    params.append(request.args.get('id').encode('utf-8'))
    update_port_threshold_table(params)
    result = show_port_thresholdset_table()
    return dict(success=True, data=result)