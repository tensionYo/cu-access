# encoding=utf-8
from flask.blueprints import Blueprint
from blueprint.olt_service import *
from flask import request

bp = Blueprint('olt-bp', __name__, url_prefix='/api')


@bp.route('/menus/')
def get_menus():
    return menus()


@bp.route('/menus/department/')
def get_departments():
    return menu_department()


@bp.route('/menus/<city_name>/<department_name>/')
def get_stations(city_name, department_name):
    return menu_station(city_name.encode('utf-8'), department_name.encode('utf-8'))


@bp.route('/menus/<city_name>/<department_name>/<station>/')
def get_olts(city_name, department_name, station):
    return menus_olt(city_name.encode('utf-8'), department_name.encode('utf-8'), station)


@bp.route('/olt-count/')
def olt_count_api():
    return olt_count('')


@bp.route('/olt-vendor-count/')
def olt_vendor_count_api():
    return olt_manufacturer_count('')


@bp.route('/olt-user-count/')
def olt_user_count_api():
    return olt_user_count('')


@bp.route('/olt-vendor-model-count/')
def olt_vendor_model_count_api():
    return olt_vendor_branch_distribution('')


@bp.route('/pon-port-count/')
def pon_port_count_api():
    return pon_port_count('')


@bp.route('/pon-port-stat/')
def pon_port_usage_rate_api():
    return pon_port_usage_rate('')


@bp.route('/service-board-stat/')
def service_board_rate_api():
    return service_board_usage_rate('')


@bp.route('/pon-type/')
def pon_type_api():
    olt = request.args.get('olt', None)
    station = request.args.get('station', None)
    department = request.args.get('department', None)
    city = request.args.get('city', None)
    return pon_type(olt, station, department, city)


@bp.route('/vendor-pon-type/')
def vendor_pon_type_api():
    station = request.args.get('station', None)
    department = request.args.get('department', None)
    city = request.args.get('city', None)
    return vendor_pon_type(station, department, city)


@bp.route('/service-board-slot-stat/')
def service_board_slot_stat_api():
    station = request.args.get('station', None)
    department = request.args.get('department', None)
    city = request.args.get('city', None)
    # TODO
    return service_board_slot_stat(station, department, city)


@bp.route('/pon-port-traffic-stat/')
def pon_port_traffic_stat_api():
    station = request.args.get('station', None)
    department = request.args.get('department', None)
    city = request.args.get('city', None)
    olt = request.args.get('olt', None)
    return pon_port_traffic_stat(olt, station, department, city)


@bp.route('/pon-port-users-stat/')
def pon_port_users_stat_api():
    station = request.args.get('station', None)
    department = request.args.get('department', None)
    city = request.args.get('city', None)
    olt = request.args.get('olt', None)
    return pon_port_users_stat(olt, station, department, city)


@bp.route('/pon-port-users-count/')
def pon_port_users_count_api():
    # DEPRECATED
    station = request.args.get('station', None)
    department = request.args.get('department', None)
    city = request.args.get('city', None)
    olt = request.args.get('olt', None)
    return pon_port_users_count(olt, station, department, city)


@bp.route('/olt-uplink-port-count/')
def olt_uplink_port_count_api():
    station = request.args.get('station', None)
    department = request.args.get('department', None)
    city = request.args.get('city', None)
    olt = request.args.get('olt', None)
    return olt_uplink_port_count(olt, station, department, city)


@bp.route('/olt-uplink/10ge/count/')
def olt_10ge_uplink_count_api():
    station = request.args.get('station', None)
    department = request.args.get('department', None)
    city = request.args.get('city', None)
    return olt_10ge_uplink_count(station, department, city)


@bp.route('/olt-uplink-stat/')
def olt_uplink_stat_api():
    station = request.args.get('station', None)
    department = request.args.get('department', None)
    city = request.args.get('city', None)
    return olt_uplink_stat(station, department, city)


# @bp.route('/olt/info/')
# def olt_info_api():
#     olt_name = request.args.get('olt_name', None)
#     return olt_info(olt_name)
