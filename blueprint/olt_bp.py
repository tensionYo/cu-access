# -*- coding: utf-8 -*-
from flask.blueprints import Blueprint
from blueprint.olt_service import *
from flask import request
from utils.decorator import json_resp, admin_role

bp = Blueprint('olt-bp', __name__, url_prefix='/api')

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


@bp.route('/<department>/<speed>/history/')
def department_speed_history(department, speed):
    """
    :type department: str
    :type speed: str
    :param department:
    :param speed:
    :return:
    """
    department = department.encode('utf-8')
    speed = speed.encode('utf-8')
    if department == '0':
        return get_all_pon_port_history_for_tianjin(speed)
    return get_department_speed_history(department, speed)

# @bp.route('/olt/info/')
# def olt_info_api():
#     olt_name = request.args.get('olt_name', None)
#     return olt_info(olt_name)

"""all network"""
@bp.route('/city_up_road_traffic/')
@json_resp
def city_up_road_traffic():
    city_up_road_traffic_impl()
    return dict(success=True, data=city_up_road_traffic_impl())




@bp.route('/pon_port_over_threshold/')
@json_resp
def pon_port_over_threshold():
    station = request.args.get('station', None)
    department = request.args.get('department_name', None)
    city = request.args.get('city_name', None)
    olt = request.args.get('olt_name', None)
    res = pon_port_over_threshold_impl(olt, station, department, city)
    return dict(success=True, data=res)

"""all network"""
@bp.route('/olt_up_port_over_threshold/')
@json_resp
def olt_up_port_over_threshold():
    olt_ip = request.args.get('olt_ip', None)
    return olt_up_port_over_threshold_impl(olt_ip)

@bp.route('/pon_port_lowwer_than_threshold/')
@json_resp
def pon_port_lowwer_than_threshold():
    station = request.args.get('station', None)
    department = request.args.get('department_name', None)
    city = request.args.get('city_name', None)
    olt = request.args.get('olt_name', None)
    return pon_port_lowwer_than_threshold_impl(olt, station, department, city)

"""all network"""
@bp.route('/olt_up_port_lowwer_than_threshold/')
@json_resp
def olt_up_port_lowwer_than_threshold():
    return dict(success=True, data=olt_up_port_lowwer_than_threshold_impl())


"""all network"""
@bp.route('/bras_8_3/')
@json_resp
def bras_8_3():
    return bras_8_3_impl()

"""all network"""
@bp.route('/CDN_8_3/')
@json_resp
def CDN_8_3():
    return CDN_8_3_impl()

"""all network"""
@bp.route('/PON_traffic_trend_line_8_4/')
@json_resp
def PON_traffic_trend_line_8_4():
    return dict(success=True, data=PON_traffic_trend_line_8_4_impl())

"""all network"""
@bp.route('/user_featrue_trend_line_8_5/')
@json_resp
def user_featrue_trend_line_8_5():
    return user_featrue_trend_line_8_5_impl()


@bp.route('/user_type_ratio_8_7/')
@json_resp
def user_type_ratio_8_7():
    return dict(success=True, data=user_type_ratio_8_7_impl())

"""all network"""
@bp.route('/trunk_statistics_8_14/')
@json_resp
def trunk_statistics_8_14():
    return dict(success=True, data=trunk_statistics_8_14_impl())


@bp.route('/station_select_8_16pre/')
@json_resp
def station_select_8_16pre():
    return dict(success=True, data=station_select_8_16pre_impl())


"""all network"""
@bp.route('/pon_occupy_8_16/')
@json_resp
def pon_occupy_8_16():
    station = request.args.get('station', None)
    print(station)
    return dict(success=True, data=pon_occupy_8_16_impl(station))

@bp.route('/pre_show_table_9_1/')
@json_resp
def pre_show_table_9_1():
    return dict(success=True, data=pre_show_table_9_1_impl())

DEFAULT_EMPTY = '--EMPTY--'
# ratio_table_9_1_KEYS = ['user_type','user_speed','ratio']
@bp.route('/pre_modified_ratio_table_9_1/')
@json_resp
def pre_modified_ratio_table_9_1():
    params = []
    # for k in ratio_table_9_1_KEYS:
    #     params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    params.append(request.args.get('ratio').encode('utf-8'))
    params.append(request.args.get('id').encode('utf-8'))
    print(params)
    pre_modified_ratio_table_9_1_impl(params)
    return dict(success=True, data=pre_show_table_9_1_impl())


@bp.route('/pre_modified_meal_table_9_1/')
@json_resp
def pre_modified_meal_table_9_1():
    params = []
    # for k in ratio_table_9_1_KEYS:
    #     params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    params.append(request.args.get('200M').encode('utf-8'))
    params.append(request.args.get('300M').encode('utf-8'))
    params.append(request.args.get('500M').encode('utf-8'))
    params.append(request.args.get('1G').encode('utf-8'))
    print(params)
    pre_modified_meal_table_9_1_impl(params)
    return dict(success=True, data=pre_show_table_9_1_impl())

params_table_9_1_KEYS=['vedio_user_infiltrate_rate','vedio_concurrence_rate','boardband_concurrence_rate',
              '4K_rate','HD_rate','SD_rate','demand_user_avg_bandwidth',
              'peak_time_live_user_rate','peak_time_demand_user_rate']

@bp.route('/pre_modified_params_table_9_1/')
@json_resp
def pre_modified_params_table_9_1():
    params = []
    for k in params_table_9_1_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    #params.append(request.args.get('id').encode('utf-8'))
    print(params)
    pre_modified_params_table_9_1_impl(params)
    return dict(success=True, data=pre_show_table_9_1_impl())

@bp.route('/update_user_table_9_1/')
@json_resp
def update_user_table_9_1():
    update_user_tabe_params()
    return dict(success=True, msg='ok')


"""all network"""
@bp.route('/user_table_9_1/')
@json_resp
def user_table_9_1():
    return dict(success=True, data=user_table_9_1_impl())

"""all network"""
@bp.route('/MDU_table_9_1/')
@json_resp
def MDU_table_9_1():
    return dict(success=True, data=MDU_table_9_1_impl())


"""all network"""
@bp.route('/PON_table_9_1/')
@json_resp
def PON_table_9_1():
    return dict(success=True, data=PON_table_9_1_impl())

"""all network"""
@bp.route('/OLT_UP_table_9_1/')
@json_resp
def OLT_UP_table_9_1():
    return dict(success=True, data=OLT_UP_table_9_1_impl())

@bp.route('/user_bandwidth_model_table_show_9_11/')
@json_resp
def user_bandwidth_model_table_show_9_11():
    return dict(success=True, data=user_bandwidth_model_table_show_9_11_impl())

DEFAULT_EMPTY = '--EMPTY--'
model_KEYS = ['model_type','vedio_user_infiltrate_rate','vedio_concurrence_rate','boardband_concurrence_rate','boardband_user_avg_down',
              'live_4K','live_HD','live_SD','demand_user_avg_down','peak_time_live_user_ratio','peak_time_demand_user_ratio',
              'vedio_avg_down','boardband_avg_down','sum_down']

@bp.route('/user_bandwidth_model_table_update_9_11/')
@json_resp
def user_bandwidth_model_table_update_9_11():
    params = []
    for k in model_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    params.append(request.args.get('id').encode('utf-8'))
    user_bandwidth_model_table_update_9_11_impl(params)
    return dict(success=True, data=user_bandwidth_model_table_show_9_11_impl())

@bp.route('/show_olt_9_16/')
@json_resp
def show_olt_9_16():
    return dict(success=True, data=show_olt_9_16_impl())

@bp.route('/select_olt_and_show_pon_9_16/')
@json_resp
def select_olt_and_show_pon_9_16():
    olt_ip = request.args.get('olt_ip').encode('utf-8')
    return dict(success=True, data=select_olt_and_show_pon_9_16_impl(olt_ip))


@bp.route('/select_pon_and_show_mdu_9_16/')

def select_pon_and_show_mdu_9_16():
    olt_ip = request.args.get('olt_ip').encode('utf-8')
    olt_port = request.args.get('olt_port').encode('utf-8')
    params = [olt_ip,olt_port]
    return select_pon_and_show_mdu_9_16_impl(params)

@bp.route('/show_datas_9_16/')
@json_resp
def show_datas_9_16():
    olt_ip = request.args.get('olt_ip', None)
    olt_port = request.args.get('olt_port', None)
    mdu_ip = request.args.get('mdu_ip', None)
    res = show_datas_9_16_impl(olt_ip,olt_port,mdu_ip)
    return dict(success=True, data=res)


"""all network"""
@bp.route('/OLT_allow_usernum_10_3/')
@json_resp
def OLT_allow_usernum_10_3():
    return dict(success=True, data=OLT_allow_usernum_10_3_impl())


""""""
@bp.route('/show_ratio_10_4/')
@json_resp
def show_ratio_10_4():
    return dict(success=True, data=show_ratio_10_4_impl())

@bp.route('/modified_ratio_10_4/')
@json_resp
def modified_ratio_10_4():
    params = []
    params.append(request.args.get('200M').encode('utf-8'))
    params.append(request.args.get('300M').encode('utf-8'))
    params.append(request.args.get('500M').encode('utf-8'))
    return dict(success=True, data=modified_ratio_10_4_impl(params))


@bp.route('/select_user_by_speed_10_4/')
@json_resp
def select_user_by_speed_10_4():
    OLT_IP = request.args.get('OLT_IP')
    print(OLT_IP)
    return dict(success=True, data=select_user_by_speed_10_4_impl(OLT_IP))
"""改两个表，pre_modified_ratio_table_9_1和上面的两个接口"""

@bp.route('/cal_meal_case1_10_4/')
@json_resp
def cal_meal_case1_10_4():
    lan_user_number = request.args.get('lan_user_number',None)
    ftth_user_number = request.args.get('ftth_user_number', None)
    total_bandwidth = request.args.get('total_bandwidth',None)
    print(lan_user_number)
    print(ftth_user_number)
    print(total_bandwidth)
    res = cal_meal_case1_10_4_impl(lan_user_number,ftth_user_number,total_bandwidth)
    return dict(success=True, data=res)

@bp.route('/recommned_meal_case1_10_4/')
@json_resp
def recommned_meal_case1_10_4():
    """考虑了1.5G沉降带宽，但是ftth和lan用户流量不做区分"""
    user_num = request.args.get('user_number',None)
    print(user_num)
    total_bandwidth = request.args.get('total_bandwidth',None)
    print(total_bandwidth)
    res = recommned_meal_case1_10_4_impl(user_num,total_bandwidth)
    temp = []
    temp.append(res)
    return dict(success=True, data=temp)

@bp.route('/device_ability_11_1/')
@json_resp
def device_ability_11_1():
    res = device_ability_11_1_impl()
    return dict(success=True, data=res)

@bp.route('/plan_11_2/')
@json_resp
def plan_11_2():
    res = plan_11_2_impl()
    return dict(success=True, data=res)

@bp.route('/cut_11_3/')
@json_resp
def cut_11_3():
    res = cut_11_3_impl()
    return dict(success=True, data=res)

@bp.route('/plan_12_1/')
@json_resp
def plan_12_1():
    res = plan_12_1_impl()
    return dict(success=True, data=res)