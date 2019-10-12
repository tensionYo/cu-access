# encoding = utf-8
from flask import Blueprint, request
from db.client import cli
from utils.decorator import json_resp

from blueprint.aaa_service import *

bp = Blueprint('aaa_bp', __name__, url_prefix='/api/aaa')

TOP_K = {
    '10': 0.1,
    '100': 0.01,
    '1000': 0.001
}

INTERVAL = {
    '1': 1,
    '2': 2,
    '5': 5,
    '10': 10
}

TREND_TAG = ['input_avg', 'input_peak', 'output_avg', 'output_peak']


@bp.route('/top-k/')
@json_resp
def get_top_k():
    dp = request.args.get('department', '').encode('utf-8')
    st = request.args.get('station', '').encode('utf-8')
    dt = request.args.get('date', '').encode('utf-8')
    k = request.args.get('k', '').encode('utf-8')
    k = TOP_K.get(k, 0.001)
    resp = get_top_k_aaa_user(dp, st, dt, k)
    return dict(success=True, data=resp)


@bp.route('/pon-statistics/')
@json_resp
def get_pon_port_statistics():
    city_name = request.args.get('city_name', '').encode('utf-8')
    department_name = request.args.get('department_name', '').encode('utf-8')
    interval = request.args.get('interval', '').encode('utf-8')
    r = get_pon_port_traffic_statistics(city_name, department_name, INTERVAL.get(interval, 5))
    return dict(success=True, data=r)


@bp.route('/pon-port/trend/')
@json_resp
def get_trend():
    city_name = request.args.get('city_name', '').encode('utf-8')
    department = request.args.get('department_name', '').encode('utf-8')
    station = request.args.get('station', '').encode('utf-8')
    olt = request.args.get('olt_name', '').encode('utf-8')
    tag = request.args.get('tag', '').encode('utf8')
    tag = tag if tag in TREND_TAG else 'input_avg'
    r = get_pon_trend(city_name, department, station, olt, tag)
    return dict(success=True, data=r)
