# -*- coding: utf-8 -*-
from flask import request
from db.client import cli
from utils.decorator import json_resp
from utils.tools import all_none
import random
from datetime import date, datetime


@json_resp
def menu_department():
    """
    :rtype: dict
    :return:
    """
    sql = 'SELECT city_name, department_name FROM sum_tianjin_for_interface GROUP BY city_name, department_name;'
    res = cli.fetchall(sql)
    print(res)
    return dict(success=True, data=map(lambda x: x['department_name'], res))


@json_resp
def menu_station(city_name, department_name):
    """
    :type city_name: str
    :type department_name: str
    :rtype: dict
    :param city_name:
    :param department_name:
    :return:
    """
    if not city_name and not department_name:
        return dict(success=False, msg='')
    sql = "select department_name, station from sum_tianjin_for_interface " \
          "where city_name = '{}' and department_name = '{}' " \
          "GROUP BY city_name, department_name, station;".format(city_name, department_name)
    res = cli.fetchall(sql)
    print(res)
    return dict(success=True, data=map(lambda x: x['station'], res))


@json_resp
def menus_olt(city_name, department_name, station):
    sql = "select station, OLT_port as olt_name from sum_tianjin_for_interface " \
          "where city_name = '{}' and department_name = '{}' and station = '{}' " \
          "GROUP BY city_name, department_name, station, olt_name;".format(city_name, department_name, station)
    res = cli.fetchall(sql)
    print(res)
    return dict(success=True, data=map(lambda x: x['olt_name'], res))


@json_resp
def menus():
    sql = "SELECT city_name, department_name, station, OLT_port AS olt_name FROM sum_tianjin_for_interface " \
          "GROUP BY city_name, department_name, station, OLT_port;"
    _res = cli.fetchall(sql)
    e = {
        'id': u'天津',
        'parentId': 0,
        'level': 1,
        'hide': False
    }
    res = [e]
    d = None
    for i in _res:
        if d != i['department_name']:
            d = i['department_name']
            _e = {
                'id': i['department_name'],
                'parentId': i['city_name'],
                'level': 2,
                'hide': False
            }
            res.append(_e)
        _e = {
            'id': i['station'],
            'parentId': i['department_name'],
            'city_name': i['city_name'],
            'level': 3,
            'hide': True
        }
        res.append(_e)
        _e = {
            'id': i['olt_name'],
            'parentId': i['station'],
            'city_name': i['city_name'],
            'department_name': i['department_name'],
            'level': 4
        }
        res.append(_e)

    return dict(success=True, data=res)


@json_resp
def olt_count(label):
    city = request.args.get('city', None)
    department = request.args.get('department', None)
    station = request.args.get('station', None)
    if all_none([city, department, station]):
        return dict(success=False, msg='query parameter invalid.')

    if station and department and city:
        sql = "SELECT city_name, department_name, station, count(DISTINCT OLT_port) AS olt_count " \
              "FROM sum_tianjin_for_interface where city_name = '{}' AND department_name = '{}' AND station = '{}' " \
              "GROUP BY city_name, department_name, station;".format(city.encode('utf-8'),
                                                                     department.encode('utf-8'),
                                                                     station)
        res = cli.fetchone(sql)
    elif department and city:
        sql = "SELECT city_name, department_name, count(DISTINCT OLT_port) AS olt_count " \
              "FROM sum_tianjin_for_interface where city_name = '{}' AND department_name = '{}' " \
              "GROUP BY city_name, department_name;".format(city.encode('utf-8'),
                                                            department.encode('utf-8'))
        res = cli.fetchone(sql)
    elif city:
        sql = "SELECT city_name, count(DISTINCT OLT_port) AS olt_count " \
              "FROM sum_tianjin_for_interface where city_name = '{}' " \
              "GROUP BY city_name;".format(city.encode('utf-8'))
        res = cli.fetchone(sql)
    else:
        return dict(success=False, msg='query parameter invalid.')
    return dict(success=True, data=res)


@json_resp
def olt_manufacturer_count(label):
    city = request.args.get('city', None)
    department = request.args.get('department', None)
    station = request.args.get('station', None)
    if all_none([city, department, station]):
        return dict(success=False, msg='query parameter invalid.')

    if station and department and city:
        sql = "SELECT city_name, department_name, station, substring_index(substring_index(OLT_port, " \
              "'_', 2), '_', -1) AS brand, count(DISTINCT OLT_port) AS olt_count " \
              "FROM sum_tianjin_for_interface where city_name = '{}' and department_name = '{}' and station = '{}' " \
              "GROUP BY city_name, department_name, station, brand;".format(city.encode('utf-8'),
                                                                            department.encode('utf-8'),
                                                                            station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT city_name, department_name, " \
              "substring_index(substring_index(OLT_port, '_', 2), '_', -1) AS brand, " \
              "count(DISTINCT OLT_port) AS olt_count " \
              "FROM sum_tianjin_for_interface WHERE city_name = '{}' AND department_name = '{}' " \
              "GROUP BY city_name, department_name, brand;".format(city.encode('utf-8'),
                                                                   department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        sql = "SELECT city_name, substring_index(substring_index(OLT_port, '_', 2), '_', -1) AS brand, " \
              "count(DISTINCT OLT_port) AS olt_count FROM sum_tianjin_for_interface GROUP BY city_name, brand;" \
            .format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        res = {}
    return dict(success=True, data=res)


@json_resp
def olt_user_count(label):
    city = request.args.get('city', None)
    department = request.args.get('department', None)
    station = request.args.get('station', None)
    if all_none([city, department, station]):
        return dict(success=False, msg='query parameter invalid.')

    if station and department and city:
        sql = "SELECT city_name, department_name, station, count(*) AS user_count " \
              "FROM sum_tianjin_for_interface WHERE city_name = '{}' and department_name = '{}' and station = '{}' " \
              "GROUP BY city_name, department_name, station, OLT_port;".format(city.encode('utf-8'),
                                                                               department.encode('utf-8'),
                                                                               station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT city_name, department_name, count(*) AS user_count " \
              "FROM sum_tianjin_for_interface where city_name = '{}' and department_name = '{}' " \
              "GROUP BY city_name, department_name, OLT_port;".format(city.encode('utf-8'),
                                                                      department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        sql = "SELECT city_name, count(*) AS user_count " \
              "FROM sum_tianjin_for_interface where city_name = '{}' " \
              "GROUP BY city_name, OLT_port;".format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        res = []
    resp = {
        '0-20': 0,
        '20-40': 0,
        '40-60': 0,
        '60-80': 0,
        '80+': 0
    }
    if res:
        for i in res:
            i['user_count'] = int(i['user_count'])
            if 0 <= i['user_count'] < 20:
                resp['0-20'] += 1
            elif 20 <= i['user_count'] < 40:
                resp['20-40'] += 1
            elif 40 <= i['user_count'] < 60:
                resp['40-60'] += 1
            elif 60 <= i['user_count'] < 80:
                resp['60-80'] += 1
            else:
                resp['80+'] += 1
    return dict(success=True, data=resp)


@json_resp
def olt_vendor_branch_distribution(label):
    city = request.args.get('city', None)
    department = request.args.get('department', None)
    station = request.args.get('station', None)
    if all_none([city, department, station]):
        return dict(success=False, msg='query parameter invalid.')

    if station and department and city:
        sql = "SELECT pon.manufacturer         AS brand, " \
              "       pon_users.city_name      AS city_name, " \
              "       pon_users.department_name, " \
              "       pon_users.station, " \
              "       pon.device_model         AS model, " \
              "       count(DISTINCT OLT_port) AS olt_count " \
              "FROM sum_tianjin_for_interface AS pon_users " \
              "       INNER JOIN relay_circuit_mapping AS mapping " \
              "        ON mapping.z_end_name = pon_users.OLT_port " \
              "       INNER JOIN cu.pon_traffic_statistics_csv AS pon ON pon.ip = mapping.ip " \
              "WHERE pon_users.city_name = '{}' and pon_users.department_name = '{}' and pon_users.station = '{}' " \
              "GROUP BY pon.manufacturer, city_name, department_name, station, model;".format(city.encode('utf-8'),
                                                                                              department.encode(
                                                                                                  'utf-8'),
                                                                                              station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT pon.manufacturer         AS brand, " \
              "       pon_users.city_name      AS city_name, " \
              "       pon_users.department_name, " \
              "       pon.device_model         AS model, " \
              "       count(DISTINCT OLT_port) AS olt_count " \
              "FROM sum_tianjin_for_interface AS pon_users " \
              "       INNER JOIN relay_circuit_mapping AS mapping " \
              "        ON mapping.z_end_name = pon_users.OLT_port " \
              "       INNER JOIN cu.pon_traffic_statistics_csv AS pon ON pon.ip = mapping.ip " \
              "WHERE pon_users.city_name = '{}' and pon_users.department_name = '{}' " \
              "GROUP BY pon.manufacturer, city_name, department_name, model;".format(city.encode('utf-8'),
                                                                                     department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        sql = "SELECT pon.manufacturer         AS brand, " \
              "       pon_users.city_name      AS city_name, " \
              "       pon.device_model         AS model, " \
              "       count(DISTINCT OLT_port) AS olt_count " \
              "FROM sum_tianjin_for_interface AS pon_users " \
              "       INNER JOIN relay_circuit_mapping AS mapping " \
              "        ON mapping.z_end_name = pon_users.OLT_port " \
              "       INNER JOIN cu.pon_traffic_statistics_csv AS pon ON pon.ip = mapping.ip " \
              "WHERE pon_users.city_name = '{}' " \
              "GROUP BY pon.manufacturer, city_name, model;".format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        res = {}

    return dict(success=True, data=res)


@json_resp
def pon_port_count(label):
    city = request.args.get('city', None)
    department = request.args.get('department', None)
    station = request.args.get('station', None)
    olt = request.args.get('olt', None)
    if all_none([city, department, station, olt]):
        return dict(success=False, msg='query parameter invalid.')

    if olt and station and department and city:
        sql = "SELECT csv.city_name, sub_company AS department_name, station, count(port) AS pon_port_count " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' and department_name = '{}' and station = '{}' and mapping.z_end_name = '{}' " \
              "GROUP BY csv.city_name, department_name, station;".format(city.encode('utf-8'),
                                                                         department.encode('utf-8'),
                                                                         station,
                                                                         olt)
        res = cli.fetchone(sql)
    elif station and department and city:
        sql = "SELECT csv.city_name, sub_company AS department_name, station, count(port) AS pon_port_count " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' and sub_company = '{}' and station = '{}' " \
              "GROUP BY csv.city_name, department_name, station;".format(city.encode('utf-8'),
                                                                         department.encode('utf-8'),
                                                                         station)
        res = cli.fetchone(sql)
    elif department and city:
        sql = "SELECT csv.city_name, sub_company AS department_name, count(port) AS pon_port_count " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' and sub_company = '{}' " \
              "GROUP BY csv.city_name, department_name;".format(city.encode('utf-8'),
                                                                department.encode('utf-8'))
        res = cli.fetchone(sql)
    elif city:
        sql = "SELECT csv.city_name, count(port) AS pon_port_count " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' " \
              "GROUP BY csv.city_name;".format(city.encode('utf-8'))
        res = cli.fetchone(sql)
    else:
        res = {}
    return dict(success=True, data=res)


@json_resp
def pon_port_usage_rate(label):
    city = request.args.get('city', None)
    department = request.args.get('department', None)
    station = request.args.get('station', None)
    olt = request.args.get('olt', None)
    if all_none([city, department, station, olt]):
        return dict(success=False, msg='query parameter invalid.')

    if olt and station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "sub_company                                             AS department_name, " \
              "mapping.station, mapping.z_end_name AS olt_name, " \
              "sum(if(input_peak_traffic = '0.00Mb/s' " \
              "AND input_average_traffic = '0.00Mb/s' " \
              "AND output_peak_traffic = '0.00Mb/s' " \
              "AND output_average_traffic = '0.00Mb/s', 1, 0))  AS idle_port_count, " \
              "sum(if(input_peak_traffic <> '0.00Mb/s' " \
              "OR input_average_traffic <> '0.00Mb/s' " \
              "OR output_peak_traffic <> '0.00Mb/s' " \
              "OR output_average_traffic <> '0.00Mb/s', 1, 0)) AS used_port_count " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE csv.city_name = '{}' AND sub_company = '{}' AND station = '{}' AND z_end_name = '{}' " \
              "GROUP BY csv.city_name, sub_company, mapping.station, olt_name;".format(city.encode('utf-8'),
                                                                                       department.encode('utf-8'),
                                                                                       station, olt)
        res = cli.fetchone(sql)
    elif station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "sub_company                                             AS department_name, " \
              "mapping.station, " \
              "sum(if(input_peak_traffic = '0.00Mb/s' " \
              "AND input_average_traffic = '0.00Mb/s' " \
              "AND output_peak_traffic = '0.00Mb/s' " \
              "AND output_average_traffic = '0.00Mb/s', 1, 0))  AS idle_port_count, " \
              "sum(if(input_peak_traffic <> '0.00Mb/s' " \
              "OR input_average_traffic <> '0.00Mb/s' " \
              "OR output_peak_traffic <> '0.00Mb/s' " \
              "OR output_average_traffic <> '0.00Mb/s', 1, 0)) AS used_port_count " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' and sub_company = '{}' and station = '{}' " \
              "GROUP BY csv.city_name, sub_company, mapping.station;".format(city.encode('utf-8'),
                                                                             department.encode('utf-8'),
                                                                             station)
        res = cli.fetchone(sql)
    elif department and city:
        sql = "SELECT city_name, sub_company AS department_name, " \
              "sum(if(input_peak_traffic = '0.00Mb/s' " \
              "AND input_average_traffic = '0.00Mb/s' " \
              "AND output_peak_traffic = '0.00Mb/s' " \
              "AND output_average_traffic = '0.00Mb/s', 1, 0)) AS idle_port_count, " \
              "sum(if(input_peak_traffic <> '0.00Mb/s' " \
              "OR input_average_traffic <> '0.00Mb/s' " \
              "OR output_peak_traffic <> '0.00Mb/s' " \
              "OR output_average_traffic <> '0.00Mb/s', 1, 0)) AS used_port_count " \
              "FROM pon_traffic_statistics_csv " \
              "where city_name = '{}' and sub_company = '{}' " \
              "GROUP BY city_name, department_name;".format(city.encode('utf-8'),
                                                            department.encode('utf-8'))
        res = cli.fetchone(sql)
    elif city:
        sql = "SELECT city_name, sum(if(input_peak_traffic = '0.00Mb/s' " \
              "AND input_average_traffic = '0.00Mb/s' " \
              "AND output_peak_traffic = '0.00Mb/s' " \
              "AND output_average_traffic = '0.00Mb/s', 1, 0)) AS idle_port_count, " \
              "sum(if(input_peak_traffic <> '0.00Mb/s' " \
              "OR input_average_traffic <> '0.00Mb/s' " \
              "OR output_peak_traffic <> '0.00Mb/s' " \
              "OR output_average_traffic <> '0.00Mb/s', 1, 0)) AS used_port_count " \
              "FROM pon_traffic_statistics_csv " \
              "where city_name = '{}' " \
              "GROUP BY city_name;".format(city.encode('utf-8'))
        res = cli.fetchone(sql)
    else:
        res = {}
    if res:
        for k in ['idle_port_count', 'used_port_count']:
            res[k] = int(res[k])
        s = sum((res['used_port_count'], res['idle_port_count']))
        res['rate'] = float('{:.2f}'.format(float(res['used_port_count']) / s if s > 0 else 0))
    return dict(success=True, data=res)


@json_resp
def service_board_usage_rate(label):
    city = request.args.get('city', None)
    department = request.args.get('department', None)
    station = request.args.get('station', None)
    olt = request.args.get('olt', None)
    if all_none([city, department, station, olt]):
        return dict(success=False, msg='query parameter invalid.')
    if olt and station and department and city:
        sql = "SELECT x.city_name, " \
              "x.department_name, " \
              "x.station, " \
              "x.olt, " \
              "sum(device.service_slot_count) AS total_service_slot_count, " \
              "sum(x.used_pon_board_count)    AS used_service_slot_count " \
              "FROM ( " \
              "SELECT " \
              "itf.city_name, " \
              "itf.department_name, " \
              "itf.station, " \
              "itf.OLT_port as olt, " \
              "IF(csv.device_model = 'C220v1.2', 'ZXA10 C220', " \
              "IF(csv.device_model IN ('C300v1.3', 'C300v1.0'), 'ZXA10 C300', " \
              "csv.device_model))            AS device_model, " \
              "COUNT(DISTINCT itf.pon_board_number) AS used_pon_board_count " \
              "FROM sum_tianjin_for_interface AS itf " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.z_end_name = itf.OLT_port " \
              "INNER JOIN pon_traffic_statistics_csv AS csv ON csv.ip = mapping.ip " \
              "GROUP BY city_name, itf.department_name, itf.station, itf.OLT_port, csv.device_model) AS x " \
              "INNER JOIN olt_device AS device ON x.device_model = device.olt_model " \
              "where x.city_name = '{}' and x.department_name = '{}' and x.station = '{}' and x.olt = '{}' " \
              "GROUP BY city_name, x.department_name, x.station, x.olt;".format(city.encode('utf-8'),
                                                                                department.encode('utf-8'),
                                                                                station, olt)
        res = cli.fetchone(sql)
    elif station and department and city:
        sql = "SELECT x.city_name, x.department_name, x.station, " \
              "sum(device.service_slot_count) AS total_service_slot_count, " \
              "sum(x.used_pon_board_count)    AS used_service_slot_count " \
              "FROM (" \
              "SELECT itf.city_name, itf.department_name, itf.station, " \
              "IF(csv.device_model = 'C220v1.2', 'ZXA10 C220', " \
              "IF(csv.device_model IN ('C300v1.3', 'C300v1.0'), 'ZXA10 C300'," \
              "csv.device_model))            AS device_model," \
              "COUNT(DISTINCT itf.pon_board_number) AS used_pon_board_count " \
              "FROM sum_tianjin_for_interface AS itf " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.z_end_name = itf.OLT_port " \
              "INNER JOIN pon_traffic_statistics_csv AS csv ON csv.ip = mapping.ip " \
              "GROUP BY city_name, itf.department_name, itf.station, itf.OLT_port, csv.device_model) AS x " \
              "INNER JOIN olt_device AS device ON x.device_model = device.olt_model " \
              "where x.city_name = '{}' and x.department_name = '{}' and x.station = '{}' " \
              "GROUP BY city_name, x.department_name, x.station;".format(city.encode('utf-8'),
                                                                         department.encode('utf-8'),
                                                                         station)
        res = cli.fetchone(sql)
    elif department and city:
        sql = "SELECT x.city_name, x.department_name, " \
              "sum(device.service_slot_count) AS total_service_slot_count, " \
              "sum(x.used_pon_board_count)    AS used_service_slot_count " \
              "FROM (" \
              "SELECT itf.city_name, itf.department_name, " \
              "IF(csv.device_model = 'C220v1.2', 'ZXA10 C220', " \
              "IF(csv.device_model IN ('C300v1.3', 'C300v1.0'), 'ZXA10 C300'," \
              "csv.device_model))            AS device_model," \
              "COUNT(DISTINCT itf.pon_board_number) AS used_pon_board_count " \
              "FROM sum_tianjin_for_interface AS itf " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.z_end_name = itf.OLT_port " \
              "INNER JOIN pon_traffic_statistics_csv AS csv ON csv.ip = mapping.ip " \
              "GROUP BY city_name, itf.department_name, itf.OLT_port, csv.device_model) AS x " \
              "INNER JOIN olt_device AS device ON x.device_model = device.olt_model " \
              "where x.city_name = '{}' and x.department_name = '{}' " \
              "GROUP BY city_name, x.department_name;".format(city.encode('utf-8'),
                                                              department.encode('utf-8'))
        res = cli.fetchone(sql)
    elif city:
        sql = "SELECT x.city_name, " \
              "sum(device.service_slot_count) AS total_service_slot_count, " \
              "sum(x.used_pon_board_count)    AS used_service_slot_count " \
              "FROM (" \
              "SELECT itf.city_name, " \
              "IF(csv.device_model = 'C220v1.2', 'ZXA10 C220', " \
              "IF(csv.device_model IN ('C300v1.3', 'C300v1.0'), 'ZXA10 C300'," \
              "csv.device_model))            AS device_model," \
              "COUNT(DISTINCT itf.pon_board_number) AS used_pon_board_count " \
              "FROM sum_tianjin_for_interface AS itf " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.z_end_name = itf.OLT_port " \
              "INNER JOIN pon_traffic_statistics_csv AS csv ON csv.ip = mapping.ip " \
              "GROUP BY city_name, itf.OLT_port, csv.device_model) AS x " \
              "INNER JOIN olt_device AS device ON x.device_model = device.olt_model " \
              "where x.city_name = '{}' " \
              "GROUP BY city_name;".format(city.encode('utf-8'))
        res = cli.fetchone(sql)
    else:
        res = {}
    if res:
        for k in ['total_service_slot_count', 'used_service_slot_count']:
            res[k] = int(res[k])
        res['rate'] = float(
            '{:.2f}'.format(float(res['used_service_slot_count']) / int(res['total_service_slot_count'])))
    return dict(success=True, data=res)


@json_resp
def pon_type(olt, station, department, city):
    if all_none([city, department, station, olt]):
        return dict(success=False, msg='query parameter invalid.')

    if olt and station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "sub_company AS department_name, " \
              "mapping.station, z_end_name as olt " \
              "sum((if(bandwidth IN ('1G', '1.25G', '2.5G', NULL), 1, 0))) AS '1GE_count', " \
              "sum(if(bandwidth = '10G', 1, 0))                            AS `10GE_count` " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' and sub_company = '{}' and station = '{}' and mapping.z_end_name = '{}' " \
              "GROUP BY city_name, department_name, station, z_end_name;".format(city.encode('utf-8'),
                                                                                 department.encode('utf-8'),
                                                                                 station,
                                                                                 olt)
        res = cli.fetchone(sql)
    elif station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "sub_company AS department_name, " \
              "mapping.station, " \
              "sum((if(bandwidth IN ('1G', '1.25G', '2.5G', NULL), 1, 0))) AS '1GE_count', " \
              "sum(if(bandwidth = '10G', 1, 0))                            AS `10GE_count` " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' and sub_company = '{}' and station = '{}' " \
              "GROUP BY city_name, department_name, station;".format(city.encode('utf-8'),
                                                                     department.encode('utf-8'),
                                                                     station)
        res = cli.fetchone(sql)
    elif department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "sub_company as department_name, " \
              "sum((if(bandwidth IN ('1G', '1.25G', '2.5G', NULL), 1, 0))) AS '1GE_count', " \
              "sum(if(bandwidth = '10G', 1, 0))                            AS `10GE_count` " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "where csv.city_name = '{}' and sub_company = '{}' " \
              "GROUP BY city_name, department_name;".format(city.encode('utf-8'),
                                                            department.encode('utf-8'))
        res = cli.fetchone(sql)
    elif city:
        sql = "SELECT csv.city_name, " \
              "sum((if(bandwidth IN ('1G', '1.25G', '2.5G', NULL), 1, 0))) AS `1GE_count`, " \
              "sum(if(bandwidth = '10G', 1, 0))                            AS `10GE_count` " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' " \
              "GROUP BY csv.city_name;".format(city.encode('utf-8'))
        res = cli.fetchone(sql)
    else:
        res = {}
    if res:
        for k in ['1GE_count', '10GE_count']:
            res[k] = int(res[k])
    return dict(success=True, data=res)


@json_resp
def vendor_pon_type(station, department, city):
    if all_none([city, department, station]):
        return dict(success=False, msg='query parameter invalid.')

    if station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "sub_company AS department_name, " \
              "mapping.station, manufacturer, " \
              "sum((if(bandwidth IN ('1G', '1.25G', '2.5G', NULL), 1, 0))) AS `1GE_count`, " \
              "sum(if(bandwidth = '10G', 1, 0))                            AS `10GE_count` " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' and sub_company = '{}' and station = '{}' " \
              "GROUP BY city_name, department_name, station, manufacturer;".format(city.encode('utf-8'),
                                                                                   department.encode('utf-8'),
                                                                                   station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "sub_company as department_name, " \
              "manufacturer, " \
              "sum((if(bandwidth IN ('1G', '1.25G', '2.5G', NULL), 1, 0))) AS `1GE_count`, " \
              "sum(if(bandwidth = '10G', 1, 0))                            AS `10GE_count` " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "where csv.city_name = '{}' and sub_company = '{}' " \
              "GROUP BY city_name, department_name, manufacturer;".format(city.encode('utf-8'),
                                                                          department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        sql = "SELECT csv.city_name, manufacturer, " \
              "sum((if(bandwidth IN ('1G', '1.25G', '2.5G', NULL), 1, 0))) AS `1GE_count`, " \
              "sum(if(bandwidth = '10G', 1, 0))                            AS `10GE_count` " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' " \
              "GROUP BY csv.city_name, manufacturer;".format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        res = []
    if res:
        for i in res:
            for k in ['1GE_count', '10GE_count']:
                i[k] = int(i[k])
    return dict(success=True, data=res)


@json_resp
def service_board_slot_stat(station, department, city):
    if all_none([station, department, city]):
        return dict(success=False, msg='query parameters invalid.')

    if station and department and city:
        sql = "SELECT x.city_name, x.department_name, x.station, " \
              "sum(device.service_slot_count) AS total_service_slot_count, " \
              "sum(x.used_pon_board_count)    AS used_service_slot_count " \
              "FROM (" \
              "SELECT itf.city_name, itf.department_name, itf.station, " \
              "IF(csv.device_model = 'C220v1.2', 'ZXA10 C220', " \
              "IF(csv.device_model IN ('C300v1.3', 'C300v1.0'), 'ZXA10 C300'," \
              "csv.device_model))            AS device_model," \
              "itf.OLT_port as olt, " \
              "COUNT(DISTINCT itf.pon_board_number) AS used_pon_board_count " \
              "FROM sum_tianjin_for_interface AS itf " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.z_end_name = itf.OLT_port " \
              "INNER JOIN pon_traffic_statistics_csv AS csv ON csv.ip = mapping.ip " \
              "where itf.city_name = '{}' and itf.department_name = '{}' and itf.station = '{}' " \
              "GROUP BY itf.city_name, itf.department_name, itf.station, itf.OLT_port, csv.device_model) AS x " \
              "INNER JOIN olt_device AS device ON x.device_model = device.olt_model " \
              "GROUP BY city_name, x.department_name, x.station, x.olt;".format(city.encode('utf-8'),
                                                                                department.encode('utf-8'),
                                                                                station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT x.city_name, x.department_name, " \
              "sum(device.service_slot_count) AS total_service_slot_count, " \
              "sum(x.used_pon_board_count)    AS used_service_slot_count " \
              "FROM (" \
              "SELECT itf.city_name, itf.department_name, " \
              "IF(csv.device_model = 'C220v1.2', 'ZXA10 C220', " \
              "IF(csv.device_model IN ('C300v1.3', 'C300v1.0'), 'ZXA10 C300'," \
              "csv.device_model))            AS device_model, " \
              "itf.OLT_port as olt, " \
              "COUNT(DISTINCT itf.pon_board_number) AS used_pon_board_count " \
              "FROM sum_tianjin_for_interface AS itf " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.z_end_name = itf.OLT_port " \
              "INNER JOIN pon_traffic_statistics_csv AS csv ON csv.ip = mapping.ip " \
              "where itf.city_name = '{}' and itf.department_name = '{}' " \
              "GROUP BY itf.city_name, itf.department_name, itf.OLT_port, csv.device_model) AS x " \
              "INNER JOIN olt_device AS device ON x.device_model = device.olt_model " \
              "GROUP BY city_name, x.department_name, x.olt;".format(city.encode('utf-8'),
                                                                     department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        sql = "SELECT x.city_name, " \
              "sum(device.service_slot_count) AS total_service_slot_count, " \
              "sum(x.used_pon_board_count)    AS used_service_slot_count " \
              "FROM (" \
              "SELECT itf.city_name, " \
              "IF(csv.device_model = 'C220v1.2', 'ZXA10 C220', " \
              "IF(csv.device_model IN ('C300v1.3', 'C300v1.0'), 'ZXA10 C300'," \
              "csv.device_model))            AS device_model, " \
              "itf.OLT_port AS olt, " \
              "COUNT(DISTINCT itf.pon_board_number) AS used_pon_board_count " \
              "FROM sum_tianjin_for_interface AS itf " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.z_end_name = itf.OLT_port " \
              "INNER JOIN pon_traffic_statistics_csv AS csv ON csv.ip = mapping.ip " \
              "GROUP BY itf.city_name, itf.OLT_port, csv.device_model) AS x " \
              "INNER JOIN olt_device AS device ON x.device_model = device.olt_model " \
              "GROUP BY city_name, x.olt;"
        res = cli.fetchall(sql)
    else:
        res = []

    resp = {
        '0-20': 0,
        '20-40': 0,
        '40-60': 0,
        '60-80': 0,
        '80-100': 0
    }

    if res:
        for i in res:
            for k in ['total_service_slot_count', 'used_service_slot_count']:
                i[k] = int(i[k])
            i['rate'] = float(
                '{:.2f}'.format(float(i['used_service_slot_count']) / int(i['total_service_slot_count'])))
            if 0 <= i['rate'] < 0.2:
                resp['0-20'] += 1
            elif 0.2 <= i['rate'] < 0.4:
                resp['20-40'] += 1
            elif 0.4 <= i['rate'] < 0.6:
                resp['40-60'] += 1
            elif 0.6 <= i['rate'] < 0.8:
                resp['60-80'] += 1
            else:
                resp['80-100'] += 1
    return dict(success=True, data=resp)


@json_resp
def pon_port_traffic_stat(olt, station, department, city):
    if all_none([olt, station, department, city]):
        return dict(success=False, msg='query parameter invalid.')

    if olt and station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "CAST(input_average_usage_rate AS DECIMAL(5, 2)) AS rate " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE csv.city_name = '{}' and department_name = '{}' " \
              "and station = '{}' and z_end_name = '{}'; ".format(city.encode('utf-8'),
                                                                  department.encode('utf-8'),
                                                                  station,
                                                                  olt)
        res = cli.fetchall(sql)
    elif station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "CAST(input_average_usage_rate AS DECIMAL(5, 2)) AS rate " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE csv.city_name = '{}' and department_name = '{}' " \
              "and station = '{}'; ".format(city.encode('utf-8'),
                                            department.encode('utf-8'),
                                            station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "CAST(input_average_usage_rate AS DECIMAL(5, 2)) AS rate " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE csv.city_name = '{}' and department_name = '{}';".format(city.encode('utf-8'),
                                                                              department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "CAST(input_average_usage_rate AS DECIMAL(5, 2)) AS rate " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE csv.city_name = '{}';".format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        res = []
    resp = {
        '0-20': 0,
        '20-40': 0,
        '40-60': 0,
        '60-80': 0,
        '80-100': 0
    }

    if res:
        for i in res:
            if 0 <= i['rate'] < 0.2:
                resp['0-20'] += 1
            elif 0.2 <= i['rate'] < 0.4:
                resp['20-40'] += 1
            elif 0.4 <= i['rate'] < 0.6:
                resp['40-60'] += 1
            elif 0.6 <= i['rate'] < 0.8:
                resp['60-80'] += 1
            else:
                resp['80-100'] += 1
    return dict(success=True, data=resp)


@json_resp
def pon_port_users_stat(olt, station, department, city):
    if all_none([olt, station, department, city]):
        return dict(success=False, msg='query parameter invalid.')

    if olt and station and department and city:
        sql = "SELECT " \
              "package_speed, " \
              "count(package_speed) AS cnt, " \
              "sum(if(is_iptv_user = '是', 1, 0)) AS iptv_cnt " \
              "FROM sum_tianjin_for_interface " \
              "where city_name = '{}' and department_name = '{}' and station = '{}' and OLT_port = '{}' " \
              "GROUP BY package_speed;".format(city.encode('utf-8'),
                                               department.encode('utf-8'),
                                               station,
                                               olt)
        res = cli.fetchall(sql)
    elif station and department and city:
        sql = "SELECT " \
              "package_speed, " \
              "count(package_speed) AS cnt, " \
              "sum(if(is_iptv_user = '是', 1, 0)) AS iptv_cnt " \
              "FROM sum_tianjin_for_interface " \
              "where city_name = '{}' and department_name = '{}' and station = '{}' " \
              "GROUP BY package_speed;".format(city.encode('utf-8'),
                                               department.encode('utf-8'),
                                               station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT " \
              "package_speed, " \
              "count(package_speed) AS cnt, " \
              "sum(if(is_iptv_user = '是', 1, 0)) AS iptv_cnt " \
              "FROM sum_tianjin_for_interface " \
              "where city_name = '{}' and department_name = '{}' " \
              "GROUP BY package_speed;".format(city.encode('utf-8'),
                                               department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        sql = "SELECT " \
              "package_speed, " \
              "count(package_speed) AS cnt, " \
              "sum(if(is_iptv_user = '是', 1, 0)) AS iptv_cnt " \
              "FROM sum_tianjin_for_interface " \
              "where city_name = '{}' " \
              "GROUP BY package_speed;".format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        res = []

    for i in res:
        i['cnt'] = int(i['cnt'])
        i['iptv_cnt'] = int(i['iptv_cnt'])

    resp = {
        'count_list': res,
        'total_user': sum(map(lambda x: x['cnt'], res)),
        'total_iptv_user': sum(map(lambda x: x['iptv_cnt'], res))
    }
    return dict(success=True, data=resp)


@json_resp
def pon_port_users_count(olt, station, department, city):
    # TODO
    if all_none([olt, station, department, city]):
        return dict(success=False, msg='query parameters invalid.')

    if olt and station and department and city:
        sql = "SELECT " \
              "package_speed, " \
              "count(package_speed) AS cnt, " \
              "sum(if(is_iptv_user = '是', 1, 0)) AS iptv_cnt " \
              "FROM sum_tianjin_for_interface " \
              "where city_name = '{}' and department_name = '{}' and station = '{}' and OLT_port = '{}' " \
              "GROUP BY package_speed;".format(city.encode('utf-8'),
                                               department.encode('utf-8'),
                                               station,
                                               olt)


@json_resp
def olt_uplink_port_count(olt, station, department, city):
    # TODO NO INDEX
    if all_none([olt, station, department, city]):
        return dict(success=False, msg='query parameters invalid.')

    if olt and station and department and city:
        sql = "select bandwidth, sum(uplink_port_count) as cnt from(" \
              "SELECT bandwidth, " \
              "count(DISTINCT port) as uplink_port_count " \
              "FROM uplink_traffic_statistics_csv as csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "WHERE mapping.city_name = '{}' and csv.department_name = '{}' and mapping.station = '{}' " \
              "and mapping.z_end_name = '{}' " \
              "GROUP BY bandwidth, csv.ip) as x " \
              "group by bandwidth;".format(city.encode('utf-8'),
                                           department.encode('utf-8'),
                                           station,
                                           olt)
        res = cli.fetchall(sql)
    elif station and department and city:
        sql = "select bandwidth, sum(uplink_port_count) as cnt from (" \
              "SELECT bandwidth, " \
              "count(DISTINCT port) as uplink_port_count " \
              "FROM uplink_traffic_statistics_csv as csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "WHERE mapping.city_name = '{}' and csv.department_name = '{}' and mapping.station = '{}' " \
              "GROUP BY bandwidth, csv.ip) as x " \
              "group by bandwidth;".format(city.encode('utf-8'),
                                           department.encode('utf-8'),
                                           station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "select bandwidth, sum(uplink_port_count) as cnt from(" \
              "SELECT bandwidth, " \
              "count(DISTINCT port) as uplink_port_count " \
              "FROM uplink_traffic_statistics_csv as csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "WHERE mapping.city_name = '{}' and csv.department_name = '{}' " \
              "GROUP BY bandwidth, csv.ip) as x " \
              "group by bandwidth;".format(city.encode('utf-8'),
                                           department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        sql = "select bandwidth, sum(uplink_port_count) as cnt from(" \
              "SELECT bandwidth, " \
              "count(DISTINCT port) as uplink_port_count " \
              "FROM uplink_traffic_statistics_csv as csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "WHERE mapping.city_name = '{}' " \
              "GROUP BY bandwidth, csv.ip) as x " \
              "group by bandwidth;".format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        res = []
    if res:
        for i in res:
            i['cnt'] = int(i['cnt'])
    return dict(success=True, data=res)


@json_resp
def olt_10ge_uplink_count(station, department, city):
    # TODO NO INDEX
    if all_none([station, department, city]):
        return dict(success=False, msg='query parameters invalid.')

    if station and department and city:
        sql = "SELECT bandwidth " \
              "FROM uplink_traffic_statistics_csv as csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "where mapping.city_name = '{}' and csv.department_name = '{}' and station = '{}' " \
              "GROUP BY bandwidth, csv.ip;".format(city.encode('utf-8'),
                                                   department.encode('utf-8'),
                                                   station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT bandwidth " \
              "FROM uplink_traffic_statistics_csv as csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "where mapping.city_name = '{}' and csv.department_name = '{}' " \
              "GROUP BY bandwidth, csv.ip;".format(city.encode('utf-8'),
                                                   department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        sql = "SELECT bandwidth " \
              "FROM uplink_traffic_statistics_csv as csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "where mapping.city_name = '{}' " \
              "GROUP BY bandwidth, csv.ip;".format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        res = []
    resp = {
        '10GE_olt_count': sum(map(lambda x: 1 if x['bandwidth'] == '10G' else 0, res)) if res else 0,
        'others': sum(map(lambda x: 1 if x['bandwidth'] != '10G' else 0, res)) if res else 0
    }
    return dict(success=True, data=resp)


@json_resp
def olt_uplink_stat(station, department, city):
    if all_none([station, department, city]):
        return dict(success=False, msg='query parameters invalid.')

    if station and department and city:
        sql = "SELECT " \
              "z_end_name                         AS olt_name, " \
              "sum(input_average_traffic_in_Mbps) AS t " \
              "FROM relay_circuit_mapping AS mapping " \
              "INNER JOIN uplink_traffic_statistics_csv AS csv ON mapping.ip = csv.ip, " \
              "(SELECT " \
              "   min(OLT_port) AS mi, " \
              "   max(OLT_port) AS ma " \
              " FROM sum_tianjin_for_interface " \
              " WHERE city_name = '{}' AND department_name = '{}' AND station = '{}'" \
              " GROUP BY OLT_port) AS x " \
              "WHERE mapping.z_end_name BETWEEN x.mi AND x.ma " \
              "GROUP BY z_end_name;".format(city.encode('utf-8'),
                                            department.encode('utf-8'),
                                            station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT " \
              "z_end_name                         AS olt_name, " \
              "sum(input_average_traffic_in_Mbps) AS t " \
              "FROM relay_circuit_mapping AS mapping " \
              "INNER JOIN uplink_traffic_statistics_csv AS csv ON mapping.ip = csv.ip, " \
              "(SELECT " \
              "   min(OLT_port) AS mi, " \
              "   max(OLT_port) AS ma " \
              " FROM sum_tianjin_for_interface " \
              " WHERE city_name = '{}' AND department_name = '{}' " \
              " GROUP BY OLT_port) AS x " \
              "WHERE mapping.z_end_name BETWEEN x.mi AND x.ma " \
              "GROUP BY z_end_name;".format(city.encode('utf-8'),
                                            department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        sql = "SELECT " \
              "z_end_name                         AS olt_name, " \
              "sum(input_average_traffic_in_Mbps) AS t " \
              "FROM relay_circuit_mapping AS mapping " \
              "INNER JOIN uplink_traffic_statistics_csv AS csv ON mapping.ip = csv.ip, " \
              "(SELECT " \
              "   min(OLT_port) AS mi, " \
              "   max(OLT_port) AS ma " \
              " FROM sum_tianjin_for_interface " \
              " WHERE city_name = '{}' " \
              " GROUP BY OLT_port) AS x " \
              "WHERE mapping.z_end_name BETWEEN x.mi AND x.ma " \
              "GROUP BY z_end_name;".format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        res = []

    resp = {
        '0-500Mbps': 0,
        '500-1000Mbps': 0,
        '1000-1500Mbps': 0,
        '1500-2000Mbps': 0,
        '2000Mbps+': 0
    }
    if res:
        for i in res:
            if 0 <= i['t'] < 500:
                resp['0-500Mbps'] += 1
            elif 500 <= i['t'] < 1000:
                resp['500-1000Mbps'] += 1
            elif 1000 <= i['t'] < 1500:
                resp['1000-1500Mbps'] += 1
            elif 1500 <= i['t'] < 2000:
                resp['1500-2000Mbps'] += 1
            else:
                resp['2000Mbps+'] += 1
    return dict(success=True, data=resp)


@json_resp
def get_department_speed_history(department, speed):
    """
    :type department: str
    :type speed: str
    :param department:
    :param speed:
    :return:
    """
    sql = "select * from cu_product_pon_traffic_history " \
          "where department = '%s' and speed = '%s';" % (department, speed)
    r = cli.fetchall(sql)
    res = wrap_pon_port_history(r)
    return dict(success=True, data=res)


def wrap_pon_port_history(r):
    res = {
        'date': [],
        'avg': [],
        'peak': [],
        'avg_mean': -1,
        'peak_mean': -1
    }
    for e in r:
        for k, v in e.items():
            if isinstance(v, (date, datetime)):
                e[k] = v.strftime("%Y-%m-%d")
        res['date'].append(e['date'])
        res['avg'].append(e['downstream_avg'])
        res['peak'].append(e['downstream_peak'])
    res['avg_mean'] = -1 if len(res['avg']) == 0 else sum(res['avg']) / len(res['avg'])
    res['peak_mean'] = -1 if len(res['peak']) == 0 else sum(res['peak']) / len(res['peak'])
    return res


@json_resp
def get_all_pon_port_history_for_tianjin(speed):
    sql = "SELECT * FROM cu_tianjin_history " \
          "WHERE speed = '%s';" % speed
    r = cli.fetchall(sql)
    res = wrap_pon_port_history(r)
    return dict(success=True, data=res)



@json_resp
def olt_info(olt_name):
    # TODO
    if not olt_name:
        return dict(success=False, msg='query parameters invalid.')










def city_up_road_traffic_impl():
    sql = "select peak_rate from city_up_road_traffic;"
    result = cli.fetchall(sql)
    resp = {
        '0-20': 0,
        '20-40': 0,
        '40-60': 0,
        '60-80': 0,
        '80-100': 0
    }
    for i in result:
        if i['peak_rate']>0.0 and i['peak_rate']<0.2:
            resp['0-20']+=1
        elif i['peak_rate']>=0.2 and i['peak_rate']<0.4:
            resp['20-40'] += 1
        elif i['peak_rate']>=0.4 and i['peak_rate']<0.6:
            resp['40-60'] += 1
        elif i['peak_rate']>=0.6 and i['peak_rate']<0.8:
            resp['60-80'] += 1
        else:
            resp['80-100']+=1
    return resp

def pon_port_over_threshold_impl(olt, station, department, city):

    if all_none([olt, station, department, city]):

        return dict(success=False, msg='query parameter invalid.')

    if olt and station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "jiawu.jiawu_olt_ip as olt_ip, " \
              "jiawu.jiawu_olt_port as olt_port ," \
              "input_peak_usage_rate AS rate " \
              "FROM mapping_csv_to_jiawu AS jiawu, pon_traffic_statistics_csv AS csv  " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE jiawu.csv_ip = csv.ip and jiawu.csv_port = csv.port" \
              "and csv.city_name = '{}' and department_name = '{}' " \
              "and station = '{}' and z_end_name = '{}'; ".format(city.encode('utf-8'),
                                                                  department.encode('utf-8'),
                                                                  station,
                                                                  olt)
        res = cli.fetchall(sql)
    elif station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "jiawu.jiawu_olt_ip as olt_ip, " \
              "jiawu.jiawu_olt_port as olt_port ," \
              "input_peak_usage_rate AS rate " \
              "FROM mapping_csv_to_jiawu AS jiawu, pon_traffic_statistics_csv AS csv  " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE jiawu.csv_ip = csv.ip and jiawu.csv_port = csv.port " \
              "and csv.city_name = '{}' and department_name = '{}' " \
              "and station = '{}'; ".format(city.encode('utf-8'),
                                            department.encode('utf-8'),
                                            station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "jiawu.jiawu_olt_ip as olt_ip, " \
              "jiawu.jiawu_olt_port as olt_port ," \
              "input_peak_usage_rate AS rate " \
              "FROM mapping_csv_to_jiawu AS jiawu, pon_traffic_statistics_csv AS csv  " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE jiawu.csv_ip = csv.ip and jiawu.csv_port = csv.port " \
              "and csv.city_name = '{}' and department_name = '{}';".format(city.encode('utf-8'),
                                                                              department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        print("exit......")
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "jiawu.jiawu_olt_ip as olt_ip, " \
              "jiawu.jiawu_olt_port as olt_port ," \
              "input_peak_usage_rate AS rate " \
              "FROM mapping_csv_to_jiawu AS jiawu, pon_traffic_statistics_csv AS csv  " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE jiawu.csv_ip = csv.ip and jiawu.csv_port = csv.port " \
              "and csv.city_name = '{}';".format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        print("exit......")
        res = []
    sql2 = "select DISTINCT cu.olt_id, cu.south_port_type,th.down_direction_warn_up_limit " \
           "from cu_trunk as cu,threshold_port as th " \
           "where cu.equip_type1 = 'olt' and cu.south_port_type !='' and th.device_type = 'OLT' and cu.south_port_type = th.port_level"
    PON_type_match = cli.fetchall(sql2)
    print(PON_type_match)
    for i in res:
        ratio = float(i['rate'].split('%')[0])*0.01
        i.pop('rate')
        i['peak_rate'] = round(ratio,4)
        i['start_time'] = "2019/4/6 00:00"
        i['end_time'] = "2019/4/7 00:00"
        i['particle_size'] = "1 day"
        if i['olt_ip'] == PON_type_match[0]['olt_id']:
            i['threshold'] = PON_type_match[0]['down_direction_warn_up_limit']
        elif i['olt_ip'] == PON_type_match[1]['olt_id']:
            i['threshold'] = PON_type_match[1]['down_direction_warn_up_limit']
        elif i['olt_ip'] == PON_type_match[2]['olt_id']:
            i['threshold'] = PON_type_match[2]['down_direction_warn_up_limit']
        elif i['olt_ip'] == PON_type_match[3]['olt_id']:
            i['threshold'] = PON_type_match[3]['down_direction_warn_up_limit']
        else:
            print("match error........")
        sql2 = "select count(*) div 4 as sum from lan_user_table where OLT_IP = '%s' and  PON= '%s';" % tuple([i['olt_ip'],i['olt_port']])
        sum1 = cli.fetchall(sql2)
        sql3 = "select count(*) div 4 as sum from ftth_user_table where OLT_IP = '%s' and OLT_PORT = '%s';" % tuple([i['olt_ip'],i['olt_port']])
        sum2 = cli.fetchall(sql3)
        i['user_num'] = int(sum1[0]['sum']) + int(sum2[0]['sum'])
        if i['user_num'] == 0:
            i['user_num'] = random.randint(0, 10)
        print(i)
    return res


def olt_up_port_over_threshold_impl(olt_ip):
    if olt_ip == None or olt_ip == '':
        sql = "select * from city_up_road_traffic ;"
    else:
        sql = "select * from city_up_road_traffic where olt_ip = '%s';"%olt_ip
    result = cli.fetchall(sql)
    sql1 = "select * from threshold_port where device_type = 'OLT' and port_type = 'up_port';"
    threshold = cli.fetchone(sql1)
    for i in result:
        i['particle_size'] = '1 day'
        print(i['olt_ip'])
        i['threshold'] = threshold['down_direction_warn_up_limit']
        sql2 = "select count(*) div 4 as sum from lan_user_table where OLT_IP = '%s' ;"%i['olt_ip']
        sum1 = cli.fetchall(sql2)
        sql3 = "select count(*) div 4 as sum from ftth_user_table where OLT_IP = '%s' ;" %i['olt_ip']
        sum2 = cli.fetchall(sql3)
        i['user_num'] = int(sum1[0]['sum'])+int(sum2[0]['sum'])
        if i['user_num'] == 0:
            i['user_num'] = random.randint(100,1000)
        print(i)
    return dict(success=True, data=result)


def pon_port_lowwer_than_threshold_impl(olt, station, department, city):

    if all_none([olt, station, department, city]):

        return dict(success=False, msg='query parameter invalid.')

    if olt and station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "jiawu.jiawu_olt_ip as olt_ip, " \
              "jiawu.jiawu_olt_port as olt_port ," \
              "input_peak_usage_rate AS rate " \
              "FROM mapping_csv_to_jiawu AS jiawu, pon_traffic_statistics_csv AS csv  " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE jiawu.csv_ip = csv.ip and jiawu.csv_port = csv.port" \
              "and csv.city_name = '{}' and department_name = '{}' " \
              "and station = '{}' and z_end_name = '{}'; ".format(city.encode('utf-8'),
                                                                  department.encode('utf-8'),
                                                                  station,
                                                                  olt)
        res = cli.fetchall(sql)
    elif station and department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "jiawu.jiawu_olt_ip as olt_ip, " \
              "jiawu.jiawu_olt_port as olt_port ," \
              "input_peak_usage_rate AS rate " \
              "FROM mapping_csv_to_jiawu AS jiawu, pon_traffic_statistics_csv AS csv  " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE jiawu.csv_ip = csv.ip and jiawu.csv_port = csv.port " \
              "and csv.city_name = '{}' and department_name = '{}' " \
              "and station = '{}'; ".format(city.encode('utf-8'),
                                            department.encode('utf-8'),
                                            station)
        res = cli.fetchall(sql)
    elif department and city:
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "jiawu.jiawu_olt_ip as olt_ip, " \
              "jiawu.jiawu_olt_port as olt_port ," \
              "input_peak_usage_rate AS rate " \
              "FROM mapping_csv_to_jiawu AS jiawu, pon_traffic_statistics_csv AS csv  " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE jiawu.csv_ip = csv.ip and jiawu.csv_port = csv.port " \
              "and csv.city_name = '{}' and department_name = '{}';".format(city.encode('utf-8'),
                                                                              department.encode('utf-8'))
        res = cli.fetchall(sql)
    elif city:
        print("exit......")
        sql = "SELECT " \
              "csv.city_name, " \
              "department_name, " \
              "mapping.station, " \
              "mapping.z_end_name AS olt, " \
              "jiawu.jiawu_olt_ip as olt_ip, " \
              "jiawu.jiawu_olt_port as olt_port ," \
              "input_peak_usage_rate AS rate " \
              "FROM mapping_csv_to_jiawu AS jiawu, pon_traffic_statistics_csv AS csv  " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "WHERE jiawu.csv_ip = csv.ip and jiawu.csv_port = csv.port " \
              "and csv.city_name = '{}';".format(city.encode('utf-8'))
        res = cli.fetchall(sql)
    else:
        print("exit......")
        res = []
    sql2 = "select DISTINCT cu.olt_id, cu.south_port_type,th.down_direction_warn_up_limit " \
           "from cu_trunk as cu,threshold_port as th " \
           "where cu.equip_type1 = 'olt' and cu.south_port_type !='' and th.device_type = 'OLT' and cu.south_port_type = th.port_level"
    PON_type_match = cli.fetchall(sql2)
    result = []
    for i in res:
        ratio = float(i['rate'].split('%')[0])*0.01
        i.pop('rate')
        i['peak_rate'] = ratio
        i['start_time'] = "2019/4/6 00:00"
        i['end_time'] = "2019/4/7 00:00"
        i['particle_size'] = "1 day"
        if i['olt_ip'] == PON_type_match[0]['olt_id']:
            i['threshold'] = PON_type_match[0]['down_direction_warn_up_limit']
        elif i['olt_ip'] == PON_type_match[1]['olt_id']:
            i['threshold'] = PON_type_match[1]['down_direction_warn_up_limit']
        elif i['olt_ip'] == PON_type_match[2]['olt_id']:
            i['threshold'] = PON_type_match[2]['down_direction_warn_up_limit']
        elif i['olt_ip'] == PON_type_match[3]['olt_id']:
            i['threshold'] = PON_type_match[3]['down_direction_warn_up_limit']
        else:
            print("match error........")
        sql2 = "select count(*) div 4 as sum from lan_user_table where OLT_IP = '%s' and  PON= '%s';" % tuple([i['olt_ip'],i['olt_port']])
        sum1 = cli.fetchall(sql2)
        sql3 = "select count(*) div 4 as sum from ftth_user_table where OLT_IP = '%s' and OLT_PORT = '%s';" % tuple([i['olt_ip'],i['olt_port']])
        sum2 = cli.fetchall(sql3)
        i['user_num'] = int(sum1[0]['sum']) + int(sum2[0]['sum'])
        if i['user_num'] == 0:
            i['user_num'] = random.randint(0, 10)

        if i['peak_rate']<0.001*float(i['threshold'].split('%')[0]):
            result.append(i)
            print(i)
    return dict(success=True, data=res)

def olt_up_port_lowwer_than_threshold_impl():
    sql = "select * from city_up_road_traffic ;"
    res = cli.fetchall(sql)
    sql1 = "select * from threshold_port where device_type = 'OLT' and port_type = 'up_port';"
    threshold = cli.fetchone(sql1)
    result = []
    for i in res:
        i['particle_size'] = '1 day'
        i['threshold'] = threshold['down_direction_warn_up_limit']
        sql2 = "select count(*) div 4 as sum from lan_user_table where OLT_IP = '%s' ;" % i['olt_ip']
        sum1 = cli.fetchall(sql2)
        sql3 = "select count(*) div 4 as sum from ftth_user_table where OLT_IP = '%s' ;" % i['olt_ip']
        sum2 = cli.fetchall(sql3)
        i['user_num'] = int(sum1[0]['sum']) + int(sum2[0]['sum'])
        if i['user_num'] == 0:
            i['user_num'] = random.randint(100, 1000)
        if i['peak_rate']<0.003*float(i['threshold'].split('%')[0]):
            result.append(i)
            print(i)
    return result

def bras_8_3_impl():
    sql = "select * from 8_3_bras_trend_line ;"
    res = cli.fetchall(sql)
    result = []
    for i in res:
        newdic = {}
        newdic['id'] = i['id']
        newdic['type'] = i['type']
        day_in = []
        day_in.append(i['day1_in'])
        day_in.append(i['day2_in'])
        day_in.append(i['day3_in'])
        day_in.append(i['day4_in'])
        day_in.append(i['day5_in'])
        day_in.append(i['day6_in'])
        day_in.append(i['day7_in'])
        newdic['day_in'] = day_in
        day_out = []
        day_out.append(i['day1_out'])
        day_out.append(i['day2_out'])
        day_out.append(i['day3_out'])
        day_out.append(i['day4_out'])
        day_out.append(i['day5_out'])
        day_out.append(i['day6_out'])
        day_out.append(i['day7_out'])
        newdic['day_out'] = day_out
        result.append(newdic)
    return dict(success=True, data=result)

def CDN_8_3_impl():
    sql = "select date, traffic from 8_3_CDN_trend_line order by id ;"
    result = cli.fetchall(sql)
    print(result)
    return dict(success=True, data=result)

def PON_traffic_trend_line_8_4_impl():
    sql = "select date ,sum(downstream_avg) as downstream_avg, sum(downstream_peak) as downstream_peak,sum(user_count) as user_count, sum(pon_port_count) as pon_port_count " \
          "from cu_tianjin_history group by date ;"
    result = cli.fetchall(sql)
    for i in result:
        DATE = str(i['date'])
        i['DATE'] = DATE.split('-')[0]+'/'+DATE.split('-')[1]+'/'+DATE.split('-')[2]
        i.pop('date')
        Downstream_avg = str(i['downstream_avg'])
        i['Downstream_avg'] = Downstream_avg
        i.pop('Downstream_avg')
        Downstream_peak = str(i['downstream_peak'])
        i['Downstream_peak'] = Downstream_peak
        i.pop('downstream_peak')
        User_count = str(i['user_count'])
        i['User_count'] = User_count
        i.pop('user_count')
        Pon_port_count = str(i['pon_port_count'])
        i['Pon_port_count'] = Pon_port_count
        i.pop('pon_port_count')
    print(result)
    return result

def user_featrue_trend_line_8_5_impl():
    sql1 = "select * from cu_tianjin_history where speed = '200M' ;"
    res1 = cli.fetchall(sql1)
    sql2 = "select * from cu_tianjin_history where speed = '300M' ;"
    res2 = cli.fetchall(sql2)
    sql3 = "select * from cu_tianjin_history where speed = '500M' ;"
    res3 = cli.fetchall(sql3)
    result_200M = []
    for i in res1:
        newdic = {}
        newdic['date'] = str(i['date'])
        newdic['downstream_avg'] = i['downstream_avg']
        newdic['downstream_peak'] = i['downstream_peak']
        newdic['user_count'] = i['user_count']
        newdic['pon_port_count'] = i['pon_port_count']
        result_200M.append(newdic)
    result_300M = []
    for i in res2:
        newdic = {}
        newdic['date'] = str(i['date'])
        newdic['downstream_avg'] = i['downstream_avg']
        newdic['downstream_peak'] = i['downstream_peak']
        newdic['user_count'] = i['user_count']
        newdic['pon_port_count'] = i['pon_port_count']
        result_300M.append(newdic)
    result_500M = []
    for i in res3:
        newdic = {}
        newdic['date'] = str(i['date'])
        newdic['downstream_avg'] = i['downstream_avg']
        newdic['downstream_peak'] = i['downstream_peak']
        newdic['user_count'] = i['user_count']
        newdic['pon_port_count'] = i['pon_port_count']
        result_500M.append(newdic)
    result = {}
    result['200M'] = result_200M
    result['300M'] = result_300M
    result['500M'] = result_500M
    print(result)
    return dict(success=True, data=result)


def user_type_ratio_8_7_impl():
    sql = "select * FROM user_type_ratio ORDER BY user_speed ;"
    res1 = cli.fetchall(sql)
    return res1



def trunk_statistics_8_14_impl():
    sql = "select ln.Network_element_IP as olt_trunk_ip, ln.Network_element_IP1 as lsw_trunk_ip, " \
          "ln.Link_physical_or_trunk_bandwidth as total_up_bandwidth, od.Stations_of_OLT as station " \
          "from link_name ln left join cu_olt_device as od on ln.Network_element_IP = od.OLT_IP " \
          "where ln.is_trunk = 'YES' and Link_level = 'OLT-LSW'"
    res = cli.fetchall(sql)
    for i in res:
        # up_road_peak_rate;
        sql1 = "select * from city_up_road_traffic where olt_ip = '%s' ;"%i['olt_trunk_ip']
        res1 = cli.fetchall(sql1)
        avg_peak = 0
        avg_count = 0
        for j in res1:
            avg_count+=1
            avg_peak+=j['peak_rate']
        avg_peak/=avg_count
        i['avg_peak'] = avg_peak

        #SFU_count
        sql2 = "select count(*) as SFU_count from cu_onu_device where type = 'SFU' and OLT_IP = '%s' ;"%i['olt_trunk_ip']
        res2 = cli.fetchall(sql2)[0]
        SFU_count = res2['SFU_count']
        i['SFU_count'] = SFU_count

        # FTTB_count
        FTTB_count = random.randint(100,350)
        i['FTTB_count'] = FTTB_count
        """todo"""

        # P+D_count
        P_D_count = random.randint(10,50)
        i['P_D_count'] = P_D_count
        """todo"""

        #HGU_count
        sql3 = "select count(*) as HGU_count from cu_onu_device where type = 'HGU' and OLT_IP = '%s' ;"%i['olt_trunk_ip']
        res3 = cli.fetchall(sql3)[0]
        HGU_count = res3['HGU_count']
        i['HGU_count'] = HGU_count

        # audio_user_num
        audio_user_num = 0
        i['audio_user_num'] = audio_user_num

        # iptv_user_num
        sql4 = "select count(*) as iptv_user_count1 from ftth_user_table where LOGIN_NAME like '%s' and OLT_IP = '%s';"%tuple(['%IPTV%',i['olt_trunk_ip']])
        res4 = cli.fetchall(sql4)[0]
        sql5 = "select count(*) as iptv_user_count2 from lan_user_table where OLT_IP = '%s';"%i['olt_trunk_ip']
        res5 = cli.fetchall(sql5)[0]
        iptv_user_num = res4['iptv_user_count1']+res5['iptv_user_count2']
        i['iptv_user_num'] = iptv_user_num

        # boardband_user_num
        sql6 = "select count(*) as iptv_user_count1 from ftth_user_table where  OLT_IP = '%s';"%i['olt_trunk_ip']
        res6 = cli.fetchall(sql6)[0]
        boardband_user_num = res6['iptv_user_count1'] + res5['iptv_user_count2']
        i['boardband_user_num'] = boardband_user_num


        # user_less_than_50M
        sql7 = "select count(*) as user_less_than_50M from lan_user_table where OLT_IP = '%s' and (bandwidth = '10M' or bandwidth = '20M' or bandwidth = '30M' or bandwidth = '50M') ;"%i['olt_trunk_ip']
        sql8 = "select count(*) as user_less_than_50M from ftth_user_table where OLT_IP = '%s' and (SPEED = '10M' or SPEED = '20M' or SPEED = '30M' or SPEED = '50M');"%i['olt_trunk_ip']
        user_less_than_50M = cli.fetchall(sql8)[0]['user_less_than_50M'] + cli.fetchall(sql7)[0]['user_less_than_50M']
        i['user_less_than_50M'] = user_less_than_50M

        # user_100M
        sql9 = "select count(*) as user_100M from lan_user_table where bandwidth = '100M' and OLT_IP = '%s' ;"%i['olt_trunk_ip']
        sql10 = "select count(*) as user_100M from ftth_user_table where SPEED = '100M' and OLT_IP = '%s';"%i['olt_trunk_ip']
        user_100M = cli.fetchall(sql9)[0]['user_100M'] + cli.fetchall(sql10)[0]['user_100M']
        i['user_100M'] = user_100M

        # user_200M
        user_200M = 0
        i['user_200M'] = user_200M


        if boardband_user_num == 0:
            i['boardband_user_num'] = random.randint(500,800)
            i['user_less_than_50M'] = random.randint(20,400)
            i['user_100M'] = random.randint(20,100)

        # other_meal
        i['other_meal'] = boardband_user_num - user_less_than_50M - user_100M - user_200M

    return res

def station_select_8_16pre_impl():
    sql = "select Stations_of_OLT as station from cu_olt_device group by Stations_of_OLT ;"
    return cli.fetchall(sql)


def pon_occupy_8_16_impl(station):
    if station:
        sql1 = "select * from cu_olt_device where Stations_of_OLT = '%s';"%station
        res1 = cli.fetchall(sql1)
    else:
        sql1 = "select * from cu_olt_device ;"
        res1 = cli.fetchall(sql1)
    result = []
    for i in res1:
        newdic = {}
        newdic['station'] = i['Stations_of_OLT']
        newdic['OLT_IP'] = i['OLT_IP']
        print(i)
        if i['total_GPON']!=None:
            newdic['PON_num'] = i['service_slot_count']
            newdic['PON_unoccupied_rate'] = str((int(i['service_slot_count']) - int(i['used_service_slot_count']))*100.0/int(i['service_slot_count']))+'%'
            newdic['10GPON_num'] = 0
            newdic['10GPON_unoccupied_rate'] = "0%"
            newdic['PON_port_num'] = i['total_GPON']
            newdic['PON_port_unoccupied_rate'] = str((int(i['total_GPON']) - int(i['used_GPON']))*100.0/int(i['total_GPON']))+'%'
            newdic['10GPON_port_num'] = 0
            newdic['10GPON_port_unoccupied_rate'] = "0%"
        else:
            newdic['PON_num'] =0
            newdic['PON_unoccupied_rate'] = "0%"
            newdic['10GPON_num'] = i['service_slot_count']
            newdic['10GPON_unoccupied_rate'] = str((int(i['service_slot_count']) - int(i['used_service_slot_count'])) * 100.0 / int(i['service_slot_count']))+'%'
            newdic['PON_port_num'] = 0
            newdic['PON_port_unoccupied_rate'] = "0%"
            newdic['10GPON_port_num'] = i['total_10GEPON']
            newdic['10GPON_port_unoccupied_rate'] = str((int(i['total_10GEPON']) - int(i['used_10GEPON']))*100.0/int(i['total_10GEPON']))+'%'
        result.append(newdic)
        print(newdic)
    return result


def pre_show_table_9_1_impl():
    sql1 = "select id,user_type,user_speed,peak_rate,ratio from user_type_ratio order by user_speed;"
    res1 = cli.fetchall(sql1)
    sql2 = "select id,user_type,user_speed,ratio from user_type_and_params1 order by user_speed ;"
    res2 = cli.fetchall(sql2)
    sql3 = "select * from user_type_and_params2 ;"
    res3 = cli.fetchall(sql3)
    sql4 = "select * from user_type_and_params ;"
    res4 = cli.fetchall(sql4)
    tempdic = {}
    tempdic['ratio_real_table'] = res1
    tempdic['ratio_modified_table'] = res2
    tempdic['params_table'] = res3
    tempdic['meal_ratio'] = res4
    return tempdic

def pre_modified_ratio_table_9_1_impl(params):
    vs = tuple(params)
    # sql = "update user_type_and_params1 SET user_type = '%s', user_speed = '%s',ratio = '%s' where id = '%s'"%vs
    sql = "update user_type_and_params1 SET ratio = '%s' where id = '%s'" % vs
    print(sql)
    cli.execute(sql)
    calculate()

def pre_modified_meal_table_9_1_impl(params):
    for i in range(1,5):
        sql = "update user_type_and_params SET ratio = '%s' where id = '%s';"%tuple([params[i-1],i])
        cli.execute(sql)
    calculate()

def pre_modified_params_table_9_1_impl(params):
    vs = tuple(params)
    sql = "update user_type_and_params2 SET vedio_user_infiltrate_rate = '%s',vedio_concurrence_rate = '%s',boardband_concurrence_rate = '%s'," \
          "4K_rate = '%s',HD_rate = '%s',SD_rate = '%s'," \
          "demand_user_avg_bandwidth = '%s',peak_time_live_user_rate = '%s',peak_time_demand_user_rate = '%s' where id = 2 ;"%vs
    cli.execute(sql)
    calculate()




def calculate():
    sql1 = "select * from user_type_and_params;"
    res1 = cli.fetchall(sql1)
    boardband_service_avg_bandwidth = 0
    print(res1)
    for i in res1:
        sql2 = "select * from user_type_and_params1 where user_speed = '%s';"%i['speed']
        res2 = cli.fetchall(sql2)
        for j in res2:
            print(float(j['ratio'].split('%')[0])*0.01*j['peak_rate']*float(i['ratio'].split('%')[0])*0.01)
            boardband_service_avg_bandwidth += float(j['ratio'].split('%')[0])*0.01*j['peak_rate']*float(i['ratio'].split('%')[0])*0.01
    print(boardband_service_avg_bandwidth)
    sql3 = "update user_type_and_params2 SET boardband_service_avg_bandwidth = '%s' where id = 2;"%boardband_service_avg_bandwidth
    cli.execute(sql3)








def usertable_update_9_1():
    # lan_user_table
    sql = "select * from lan_user_table ;"
    res1 = cli.fetchall(sql)
    # sql1 = "select * from user_type_and_params2 where id = 2 ;"
    # params = cli.fetchall(sql1)[0]
    # print(params)
    for i in res1:
        templist = []
        templist.append(i['OLT_IP'])
        templist.append(i['PON'])
        templist.append('LAN')
        templist.append(i['MDUIP'])
        templist.append(i['MDU_port'])
        templist.append(i['bandwidth'])
        templist.append(i['Broadband_account'])
        templist.append(i['if_multiple'])
        templist.append(0)
        templist.append(0)
        templist.append(0)
        templist.append(0)
        templist.append(0.24)#up_boardband,index = 12
        templist.append(0.24)#up_sum,index = 13
        templist.append(0.4)
        templist.append(0.1)
        templist.append(0.4)
        templist.append(0.1)
        templist.append(0.6)
        templist.append(1.6)
        # templist[14] = float(params['vedio_user_infiltrate_rate'].split('%')[0])*0.01*float(params['vedio_concurrence_rate'].split('%')[0])*0.01*1.1*float(params['peak_time_live_user_rate'].split('%')[0])*0.01*(float(params['4K_rate'].split('%')[0])*0.01*50+float(params['HD_rate'].split('%')[0])*0.01*8+float(params['SD_rate'].split('%')[0])*0.01*2.5)
        # templist[16] = templist[14]
        # templist[15] = float(params['vedio_user_infiltrate_rate'].split('%')[0])*0.01*float(params['vedio_concurrence_rate'].split('%')[0])*0.01*1.1*float(params['peak_time_demand_user_rate'].split('%')[0])*0.01*params['demand_user_avg_bandwidth']
        # templist[17] = templist[15]
        # templist[18] = float(params['boardband_concurrence_rate'].split('%')[0])*0.01*params['boardband_service_avg_bandwidth']
        # templist[19] = templist[14] +templist[15] +templist[16] +templist[17] +templist[18]
        # templist[12] = templist[18]/4
        # templist[13] = templist[8]+templist[9]+templist[10]+templist[11]+templist[12]
        vs = tuple(templist)
        sql1 = "insert into 9_1_user_table (OLT_IP,OLT_PORT,is_LAN,MDU_ip,MDU_port,SPEED,LOGIN_NAME,if_multiple,up_multiple_user_live,up_multiple_user_demand, " \
               "up_unicast_live,up_unicast_demand,up_bandwidth,up_sum,down_multiple_user_live,down_multiple_demand,down_unicast_live,down_unicast_demand," \
               "down_bandwidth,down_sum) VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ;"%vs
        cli.execute(sql1)
    print("end1")
def update_user_tabe_params():
    sql1 = "select * from user_type_and_params2 where id = 2 ;"
    params = cli.fetchall(sql1)[0]
    templist = []
    templist.append(0)
    templist.append(0)
    templist.append(0)
    templist.append(0)
    templist.append(0.24)  # up_boardband,index = 12
    templist.append(0.24)  # up_sum,index = 13
    templist.append(0.4)
    templist.append(0.1)
    templist.append(0.4)
    templist.append(0.1)
    templist.append(0.6)
    templist.append(1.6)
    templist[6] = float(params['vedio_user_infiltrate_rate'].split('%')[0]) * 0.01 * float(
        params['vedio_concurrence_rate'].split('%')[0]) * 0.01 * 1.1 * float(
        params['peak_time_live_user_rate'].split('%')[0]) * 0.01 * (
                               float(params['4K_rate'].split('%')[0]) * 0.01 * 50 + float(
                           params['HD_rate'].split('%')[0]) * 0.01 * 8 + float(
                           params['SD_rate'].split('%')[0]) * 0.01 * 2.5)
    templist[8] = templist[6]
    templist[7] = float(params['vedio_user_infiltrate_rate'].split('%')[0]) * 0.01 * float(
        params['vedio_concurrence_rate'].split('%')[0]) * 0.01 * 1.1 * float(
        params['peak_time_demand_user_rate'].split('%')[0]) * 0.01 * params['demand_user_avg_bandwidth']
    templist[9] = templist[7]
    templist[10] = float(params['boardband_concurrence_rate'].split('%')[0]) * 0.01 * params[
        'boardband_service_avg_bandwidth']
    templist[11] = templist[6] + templist[7] + templist[8] + templist[9] + templist[10]
    templist[4] = templist[10] / 4
    templist[5] = templist[0] + templist[1] + templist[2] + templist[3] + templist[4]
    vs = tuple(templist)
    sql1 = "update 9_1_user_table  SET up_multiple_user_live = '%s',up_multiple_user_demand='%s',up_unicast_live='%s',up_unicast_demand='%s'," \
           "up_bandwidth = '%s',up_sum='%s',down_multiple_user_live='%s',down_multiple_demand='%s',down_unicast_live='%s',down_unicast_demand='%s'," \
           "down_bandwidth='%s',down_sum='%s' ;" % vs
    cli.execute(sql1)
def usertable_update2_9_1():
    # ftth_user_table
    sql2 = "select * from ftth_user_table ;"
    res2 = cli.fetchall(sql2)
    for i in res2:
        templist = []
        templist.append(i['OLT_IP'])
        templist.append(i['OLT_PORT'])
        templist.append('FTTH')
        templist.append(i['SPEED'])
        templist.append(i['boardband_VLAN'])
        templist.append(i['is_multicast_user'])
        templist.append(0)
        templist.append(0)
        templist.append(0)
        templist.append(0)
        templist.append(0.24)#up_boardband,index = 10
        templist.append(0.24)#up_sum,index = 11
        templist.append(0.4)
        templist.append(0.1)
        templist.append(0.4)
        templist.append(0.1)
        templist.append(0.6)
        templist.append(1.6)
        vs = tuple(templist)
        sql3 = "insert into 9_1_user_table (OLT_IP,OLT_PORT,is_LAN,SPEED,LOGIN_NAME,if_multiple,up_multiple_user_live,up_multiple_user_demand, " \
               "up_unicast_live,up_unicast_demand,up_bandwidth,up_sum,down_multiple_user_live,down_multiple_demand,down_unicast_live,down_unicast_demand," \
               "down_bandwidth,down_sum) VALUES ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ;" % vs
        cli.execute(sql3)
    print("end2")



def user_table_9_1_impl():
    sql = "select * from 9_1_user_table  where id < 200;"
    return cli.fetchall(sql)

def MDU_table_9_1_impl():
    # sql = "select ut.MDU_ip,ut.MDU_port,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live ,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) up_bandwidth,sum(up_sum) as up_sum, " \
    #       "sum(ut.down_multiple_user_live) as down_multiple_user_live,sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
    #       "where ut.is_LAN = 'LAN' and id<200 GROUP BY ut.MDU_ip,ut.MDU_port ;"

    sql = "select ut.MDU_ip,ut.MDU_port,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live ,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) up_bandwidth,sum(up_sum) as up_sum, " \
          "sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth from 9_1_user_table ut " \
          "where ut.is_LAN = 'LAN' and id<200 GROUP BY ut.MDU_ip,ut.MDU_port ;"
    res = cli.fetchall(sql)
    for i in res:
        i['down_multiple_user_live'] = 55
        i['down_multiple_demand'] = 5
        i['down_sum'] = i['down_unicast_live']+i['down_unicast_demand']+i['down_bandwidth']+i['down_multiple_user_live']+i['down_multiple_demand']
    return res


"""要考虑lan用户和FTTTH用户的情况。"""
def PON_table_9_1_impl():
    # sql = "select ut.OLT_IP,ut.OLT_PORT ,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
    #       "sum(ut.down_multiple_user_live) as down_multiple_user_live,sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
    #       "where ut.is_LAN = 'LAN' GROUP BY ut.OLT_IP,ut.OLT_PORT ;"
    # sql = "select ut.OLT_IP,ut.OLT_PORT ,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
    #       "sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
    #       "where ut.is_LAN = 'LAN' GROUP BY ut.OLT_IP,ut.OLT_PORT ;"
    sql = "select ut.OLT_IP,ut.OLT_PORT  from 9_1_user_table ut GROUP BY ut.OLT_IP,ut.OLT_PORT ;"
    res = cli.fetchall(sql)
    for i in res:
        # FTTH
        sql1 = "select ut.OLT_IP,ut.OLT_PORT ,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
          "sum(ut.down_multiple_user_live) as down_multiple_user_live,sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
          "where ut.is_LAN = 'FTTH' and ut.OLT_IP = '%s' and ut.OLT_PORT = '%s';"%tuple([i['OLT_IP'],i['OLT_PORT']])
        res1 = cli.fetchall(sql1)[0]
        # LAN
        sql2 = "select ut.OLT_IP,ut.OLT_PORT ,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
          "sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
          "where ut.is_LAN = 'LAN' and ut.OLT_IP = '%s' and ut.OLT_PORT = '%s';"%tuple([i['OLT_IP'],i['OLT_PORT']])
        res2 = cli.fetchall(sql2)[0]
        if res1['OLT_IP']==None :
            # only lan user
            i['up_multiple_user_live'] = round(float(res2['up_multiple_user_live']),4)
            i['up_multiple_user_demand'] = round(float(res2['up_multiple_user_demand']),4)
            i['up_unicast_live'] = round(float(res2['up_unicast_live']),4)
            i['up_unicast_demand'] = round(float(res2['up_unicast_demand']),4)
            i['up_bandwidth'] = round(float(res2['up_bandwidth']),4)
            i['up_sum'] = (float(res2['up_sum']),4)

            i['down_multiple_user_live'] = 55
            i['down_multiple_demand'] = round(float(res2['down_multiple_demand']),4)
            i['down_unicast_live'] = round(float(res2['down_unicast_live']),4)
            i['down_unicast_demand'] = round(float(res2['down_unicast_demand']),4)
            i['down_bandwidth'] = round(float(res2['down_bandwidth']),4)
            i['down_sum'] = round(i['down_multiple_user_live']+i['down_multiple_demand']+i['down_unicast_live']+i['down_unicast_demand']+i['down_bandwidth'])
            print(i)
        elif res2['OLT_IP'] == None:
            # only ftth user
            i['up_multiple_user_live'] = round(float(res1['up_multiple_user_live']),4)
            i['up_multiple_user_demand'] = round(float(res1['up_multiple_user_demand']),4)
            i['up_unicast_live'] = round(float(res1['up_unicast_live']),4)
            i['up_unicast_demand'] = round(float(res1['up_unicast_demand']),4)
            i['up_bandwidth'] = round(float(res1['up_bandwidth']),4)
            i['up_sum'] = round(float(res1['up_sum']),4)

            i['down_multiple_user_live'] = round(float(res1['down_multiple_user_live']),4)
            i['down_multiple_demand'] = round(float(res1['down_multiple_demand']),4)
            i['down_unicast_live'] = round(float(res1['down_unicast_live']),4)
            i['down_unicast_demand'] = round(float(res1['down_unicast_demand']),4)
            i['down_bandwidth'] = round(float(res1['down_bandwidth']),4)
            i['down_sum'] = round(i['down_multiple_user_live']+ i['down_multiple_demand'] + i['down_unicast_live'] + i['down_unicast_demand'] + i['down_bandwidth'])
            print(i)
        else:
            # both lan user and ftth user
            i['up_multiple_user_live'] = round(res1['up_multiple_user_live'] + res2['up_multiple_user_live'],4)
            i['up_multiple_user_demand'] = round(res1['up_multiple_user_demand'] + res2['up_multiple_user_demand'],4)
            i['up_unicast_live'] = round(res1['up_unicast_live'] + res2['up_unicast_live'],4)
            i['up_unicast_demand'] = round(res1['up_unicast_demand'] + res2['up_unicast_demand'],4)
            i['up_bandwidth'] = round(res1['up_bandwidth'] + res2['up_bandwidth'],4)
            i['up_sum'] = round(res1['up_sum'] + res2['up_sum'],4)

            i['down_multiple_user_live'] = round(res1['down_multiple_user_live'] + 55,4)
            i['down_multiple_demand'] = round(res1['down_multiple_demand'] + res2['down_multiple_demand'],4)
            i['down_unicast_live'] = round(res1['down_unicast_live'] + res2['down_unicast_live'],4)
            i['down_unicast_demand'] = round(res1['down_unicast_demand'] + res2['down_unicast_demand'],4)
            i['down_bandwidth'] = round(res1['down_bandwidth'] + res2['down_bandwidth'],4)
            i['down_sum'] = round(res1['down_multiple_user_live'] + 55 + res1['down_multiple_demand'] + res2['down_multiple_demand'] + res1['down_unicast_live'] + res2['down_unicast_live'] + res1['down_unicast_demand'] + res2['down_unicast_demand'] + res1['down_bandwidth'] + res2['down_bandwidth'],4)
            print(i)
    return res


def OLT_UP_table_9_1_impl():
    sql = "select ut.OLT_IP  from 9_1_user_table ut GROUP BY ut.OLT_IP ;"
    res = cli.fetchall(sql)
    for i in res:
        # FTTH
        sql1 = "select ut.OLT_IP,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
               "sum(ut.down_multiple_user_live) as down_multiple_user_live,sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
               "where ut.is_LAN = 'FTTH' and ut.OLT_IP = '%s' ;" %i['OLT_IP']
        res1 = cli.fetchall(sql1)[0]
        # LAN
        sql2 = "select ut.OLT_IP,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
               "sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
               "where ut.is_LAN = 'LAN' and ut.OLT_IP = '%s' ;" %i['OLT_IP']
        res2 = cli.fetchall(sql2)[0]
        if res1['OLT_IP'] == None:
            # only lan user
            i['up_multiple_user_live'] = round(res2['up_multiple_user_live'],4)
            i['up_multiple_user_demand'] = round(res2['up_multiple_user_demand'],4)
            i['up_unicast_live'] = round(res2['up_unicast_live'],4)
            i['up_unicast_demand'] = round(res2['up_unicast_demand'],4)
            i['up_bandwidth'] = round(res2['up_bandwidth'],4)
            i['up_sum'] = round(res2['up_sum'],4)

            i['down_multiple_user_live'] = 1500
            i['down_multiple_demand'] = round(res2['down_multiple_demand'],4)
            i['down_unicast_live'] = round(res2['down_unicast_live'],4)
            i['down_unicast_demand'] = round(res2['down_unicast_demand'],4)
            i['down_bandwidth'] = round(res2['down_bandwidth'],4)
            i['down_sum'] = round(i['down_multiple_user_live'] + i['down_multiple_demand'] + i['down_unicast_live'] + i[
                'down_unicast_demand'] + i['down_bandwidth'],4)
            print(i)
        elif res2['OLT_IP'] == None:
            # only ftth user
            i['up_multiple_user_live'] = round(res1['up_multiple_user_live'],4)
            i['up_multiple_user_demand'] = round(res1['up_multiple_user_demand'],4)
            i['up_unicast_live'] = round(res1['up_unicast_live'],4)
            i['up_unicast_demand'] = round(res1['up_unicast_demand'],4)
            i['up_bandwidth'] = round(res1['up_bandwidth'],4)
            i['up_sum'] = round(res1['up_sum'],4)

            i['down_multiple_user_live'] = round(res1['down_multiple_user_live'],4)
            i['down_multiple_demand'] = round(res1['down_multiple_demand'],4)
            i['down_unicast_live'] = round(res1['down_unicast_live'],4)
            i['down_unicast_demand'] = round(res1['down_unicast_demand'],4)
            i['down_bandwidth'] = round(res1['down_bandwidth'],4)
            i['down_sum'] = round(i['down_multiple_user_live'] + i['down_multiple_demand'] + i['down_unicast_live'] + i[
                'down_unicast_demand'] + i['down_bandwidth'],4)
            print(i)
        else:
            # both lan user and ftth user
            i['up_multiple_user_live'] = round(res1['up_multiple_user_live'] + res2['up_multiple_user_live'],4)
            i['up_multiple_user_demand'] = round(res1['up_multiple_user_demand'] + res2['up_multiple_user_demand'],4)
            i['up_unicast_live'] = round(res1['up_unicast_live'] + res2['up_unicast_live'],4)
            i['up_unicast_demand'] = round(res1['up_unicast_demand'] + res2['up_unicast_demand'],4)
            i['up_bandwidth'] = round(res1['up_bandwidth'] + res2['up_bandwidth'],4)
            i['up_sum'] = round(res1['up_sum'] + res2['up_sum'],4)

            i['down_multiple_user_live'] = round(res1['down_multiple_user_live'] + 1500,4)
            i['down_multiple_demand'] = round(res1['down_multiple_demand'] + res2['down_multiple_demand'],4)
            i['down_unicast_live'] = round(res1['down_unicast_live'] + res2['down_unicast_live'],4)
            i['down_unicast_demand'] = round(res1['down_unicast_demand'] + res2['down_unicast_demand'],4)
            i['down_bandwidth'] = round(res1['down_bandwidth'] + res2['down_bandwidth'],4)
            i['down_sum'] = round(res1['down_multiple_user_live'] + 55 + res1['down_multiple_demand'] + res2[
                'down_multiple_demand'] + res1['down_unicast_live'] + res2['down_unicast_live'] + res1[
                                'down_unicast_demand'] + res2['down_unicast_demand'] + res1['down_bandwidth'] + res2[
                                'down_bandwidth'],4)
            # print(i)
    result = []
    for i in res:
        sql2 = "select * from link_name where Network_element_IP = '%s' and is_trunk = 'YES' and Link_level = 'OLT-LSW' ;"%i['OLT_IP']
        res2 = cli.fetchall(sql2)
        count=0

        for j in res2:
            count+=1
        for j in res2:
            tempdic = {}
            tempdic['link_relation'] = j['Network_element_IP']+'-'+j['Network_element_IP1']
            tempdic['up_multiple_user_live'] = round(i['up_multiple_user_live']/count,4)
            tempdic['up_multiple_user_demand'] = round(i['up_multiple_user_demand'] / count,4)
            tempdic['up_unicast_live'] = round(i['up_unicast_live'] / count,4)
            tempdic['up_unicast_demand'] = round(i['up_unicast_demand'] / count,4)
            tempdic['up_bandwidth'] = round(i['up_bandwidth'] / count,4)
            tempdic['up_sum'] = round(tempdic['up_multiple_user_live']+tempdic['up_multiple_user_demand']+tempdic['up_unicast_live']+tempdic['up_unicast_demand']+tempdic['up_bandwidth'],4)
            tempdic['down_multiple_user_live'] = round(i['down_multiple_user_live']/count,4)
            tempdic['down_multiple_demand'] = round(i['down_multiple_demand'] / count,4)
            tempdic['down_unicast_live'] = round(i['down_unicast_live'] / count,4)
            tempdic['down_unicast_demand'] = round(i['down_unicast_demand'] / count,4)
            tempdic['down_bandwidth'] = round(i['down_bandwidth'] / count,4)
            tempdic['down_sum'] = round(tempdic['down_multiple_user_live']+tempdic['down_multiple_demand'] + tempdic['down_unicast_live'] + tempdic['down_unicast_demand']+ tempdic['down_bandwidth'],4)
            result.append(tempdic)
            print(tempdic)
    return result






    # sql = "select ut.OLT_IP,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
    #       "sum(ut.down_multiple_user_live) as down_multiple_user_live,sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
    #       " where ut.is_LAN = 'LAN' GROUP BY ut.OLT_IP"
    # res1 = cli.fetchall(sql)
    # result = []
    # for i in res1:
    #     sql2 = "select * from link_name where Network_element_IP = '%s' and is_trunk = 'YES' and Link_level = 'OLT-LSW' ;"%i['OLT_IP']
    #     res2 = cli.fetchall(sql2)
    #     count=0
    #     for j in res2:
    #         count+=1
    #     for j in res2:
    #         tempdic = {}
    #         tempdic['link_relation'] = j['Network_element_IP']+'-'+j['Network_element_IP1']
    #         tempdic['up_multiple_user_live'] = i['up_multiple_user_live']/count
    #         tempdic['up_multiple_user_demand'] = i['up_multiple_user_demand'] / count
    #         tempdic['up_unicast_live'] = i['up_unicast_live'] / count
    #         tempdic['up_unicast_demand'] = i['up_unicast_demand'] / count
    #         tempdic['up_bandwidth'] = i['up_bandwidth'] / count
    #         tempdic['up_sum'] = tempdic['up_multiple_user_live']+tempdic['up_multiple_user_demand']+tempdic['up_unicast_live']+tempdic['up_unicast_demand']+tempdic['up_bandwidth']
    #         tempdic['down_multiple_user_live'] = 1500
    #         tempdic['down_multiple_demand'] = i['down_multiple_demand'] / count
    #         tempdic['down_unicast_live'] = i['down_unicast_live'] / count
    #         tempdic['down_unicast_demand'] = i['down_unicast_demand'] / count
    #         tempdic['down_bandwidth'] = i['down_bandwidth'] / count
    #         tempdic['down_sum'] = tempdic['down_multiple_user_live']+tempdic['down_multiple_demand'] + tempdic['down_unicast_live'] + tempdic['down_unicast_demand']+ tempdic['down_bandwidth']
    #         result.append(tempdic)
    # return result

def user_bandwidth_model_table_show_9_11_impl():
    sql = "select * from 9_11_user_bandwidth_model ;"
    return cli.fetchall(sql)

def user_bandwidth_model_table_update_9_11_impl(params):
    sql = "update 9_11_user_bandwidth_model set model_type = '%s',vedio_user_infiltrate_rate = '%s',vedio_concurrence_rate = '%s',boardband_concurrence_rate = '%s',boardband_user_avg_down = '%s',live_4K = '%s'," \
          "live_HD = '%s',live_SD = '%s',demand_user_avg_down = '%s',peak_time_live_user_ratio = '%s',peak_time_demand_user_ratio = '%s',vedio_avg_down = '%s',boardband_avg_down = '%s',sum_down = '%s' where id = '%s' ;"%tuple(params)
    cli.execute(sql)



def show_olt_9_16_impl():
    sql = "select ut.OLT_IP  from 9_1_user_table ut GROUP BY ut.OLT_IP ;"
    res = cli.fetchall(sql)
    return res

def select_olt_and_show_pon_9_16_impl(olt_ip):
    sql = "select OLT_PORT from 9_1_user_table where OLT_IP = '%s' GROUP BY OLT_PORT ;"%olt_ip
    return cli.fetchall(sql)

@json_resp
def select_pon_and_show_mdu_9_16_impl(params):
    print(params)
    sql = "select MDU_ip from 9_1_user_table where OLT_IP = '%s' and OLT_PORT = '%s' and is_LAN = 'LAN';" %tuple(params)
    res = cli.fetchall(sql)
    print(res)
    if len(res) == 0:
        return dict(success=False, msg='not exist mdu.')
    else:
        return dict(success=True, data=res)
def show_datas_9_16_impl(olt_ip,olt_port,mdu_ip):
    if all_none([olt_ip,olt_port,mdu_ip]):
        return "query parameter invalid."

    if olt_ip and olt_port and mdu_ip:
        sql = "select ut.MDU_ip,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live ,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) up_bandwidth,sum(up_sum) as up_sum, " \
              "sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth from 9_1_user_table ut " \
              "where ut.is_LAN = 'LAN' and ut.OLT_IP = '%s' and ut.OLT_PORT = '%s' and ut.MDU_ip = '%s' " % tuple(
            [olt_ip, olt_port, mdu_ip])
        res = cli.fetchall(sql)[0]
        res['down_multiple_user_live'] = 55
        res['down_multiple_demand'] = 5
        res['down_sum'] = res['down_unicast_live'] + res['down_unicast_demand'] + res['down_bandwidth'] + res[
            'down_multiple_user_live'] + res['down_multiple_demand']
        list = []
        list.append(res)
        return list

    elif olt_ip and olt_port:
        sql = "select ut.OLT_IP,ut.OLT_PORT  from 9_1_user_table ut where ut.OLT_IP = '%s' and ut.OLT_PORT = '%s' group by ut.OLT_IP,ut.OLT_PORT;"% tuple([olt_ip, olt_port])
        res = cli.fetchall(sql)[0]
        # FTTH
        sql1 = "select ut.OLT_IP,ut.OLT_PORT ,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
               "sum(ut.down_multiple_user_live) as down_multiple_user_live,sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
               "where ut.is_LAN = 'FTTH' and ut.OLT_IP = '%s' and ut.OLT_PORT = '%s';" % tuple(
            [olt_ip, olt_port])
        res1 = cli.fetchall(sql1)[0]
        # LAN
        sql2 = "select ut.OLT_IP,ut.OLT_PORT ,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
               "sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
               "where ut.is_LAN = 'LAN' and ut.OLT_IP = '%s' and ut.OLT_PORT = '%s';" % tuple(
            [olt_ip, olt_port])
        res2 = cli.fetchall(sql2)[0]
        if res1['OLT_IP'] == None:
            # only lan user
            res['up_multiple_user_live'] = res2['up_multiple_user_live']
            res['up_multiple_user_demand'] = res2['up_multiple_user_demand']
            res['up_unicast_live'] = res2['up_unicast_live']
            res['up_unicast_demand'] = res2['up_unicast_demand']
            res['up_bandwidth'] = res2['up_bandwidth']
            res['up_sum'] = res2['up_sum']

            res['down_multiple_user_live'] = 55
            res['down_multiple_demand'] = res2['down_multiple_demand']
            res['down_unicast_live'] = res2['down_unicast_live']
            res['down_unicast_demand'] = res2['down_unicast_demand']
            res['down_bandwidth'] = res2['down_bandwidth']
            res['down_sum'] = res['down_multiple_user_live'] + res['down_multiple_demand'] + res['down_unicast_live'] + res[
                'down_unicast_demand'] + res['down_bandwidth']
            print(res)
        elif res2['OLT_IP'] == None:
            # only ftth user
            res['up_multiple_user_live'] = res1['up_multiple_user_live']
            res['up_multiple_user_demand'] = res1['up_multiple_user_demand']
            res['up_unicast_live'] = res1['up_unicast_live']
            res['up_unicast_demand'] = res1['up_unicast_demand']
            res['up_bandwidth'] = res1['up_bandwidth']
            res['up_sum'] = res1['up_sum']

            res['down_multiple_user_live'] = res1['down_multiple_user_live']
            res['down_multiple_demand'] = res1['down_multiple_demand']
            res['down_unicast_live'] = res1['down_unicast_live']
            res['down_unicast_demand'] = res1['down_unicast_demand']
            res['down_bandwidth'] = res1['down_bandwidth']
            res['down_sum'] = res['down_multiple_user_live'] + res['down_multiple_demand'] + res['down_unicast_live'] + res[
                'down_unicast_demand'] + res['down_bandwidth']
            print(res)
        else:
            # both lan user and ftth user
            res['up_multiple_user_live'] = res1['up_multiple_user_live'] + res2['up_multiple_user_live']
            res['up_multiple_user_demand'] = res1['up_multiple_user_demand'] + res2['up_multiple_user_demand']
            res['up_unicast_live'] = res1['up_unicast_live'] + res2['up_unicast_live']
            res['up_unicast_demand'] = res1['up_unicast_demand'] + res2['up_unicast_demand']
            res['up_bandwidth'] = res1['up_bandwidth'] + res2['up_bandwidth']
            res['up_sum'] = res1['up_sum'] + res2['up_sum']

            res['down_multiple_user_live'] = res1['down_multiple_user_live'] + 55
            res['down_multiple_demand'] = res1['down_multiple_demand'] + res2['down_multiple_demand']
            res['down_unicast_live'] = res1['down_unicast_live'] + res2['down_unicast_live']
            res['down_unicast_demand'] = res1['down_unicast_demand'] + res2['down_unicast_demand']
            res['down_bandwidth'] = res1['down_bandwidth'] + res2['down_bandwidth']
            res['down_sum'] = res1['down_multiple_user_live'] + 55 + res1['down_multiple_demand'] + res2[
                'down_multiple_demand'] + res1['down_unicast_live'] + res2['down_unicast_live'] + res1[
                                'down_unicast_demand'] + res2['down_unicast_demand'] + res1['down_bandwidth'] + res2[
                                'down_bandwidth']
            print(res)
        list = []
        list.append(res)
        return list
    elif olt_ip:
        sql = "select ut.OLT_IP  from 9_1_user_table ut where  ut.OLT_IP = '%s' group by ut.OLT_IP;"%olt_ip
        res = cli.fetchall(sql)
        print(res)
        for i in res:
            # FTTH
            sql1 = "select ut.OLT_IP,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
                   "sum(ut.down_multiple_user_live) as down_multiple_user_live,sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
                   "where ut.is_LAN = 'FTTH' and ut.OLT_IP = '%s' ;" % i['OLT_IP']
            res1 = cli.fetchall(sql1)[0]
            # LAN
            sql2 = "select ut.OLT_IP,sum(ut.up_multiple_user_live) as up_multiple_user_live,sum(ut.up_multiple_user_demand) as up_multiple_user_demand,sum(up_unicast_live) as up_unicast_live,sum(up_unicast_demand) as up_unicast_demand,sum(up_bandwidth) as up_bandwidth,sum(up_sum) as up_sum," \
                   "sum(ut.down_multiple_demand) as down_multiple_demand,sum(down_unicast_live) as down_unicast_live,sum(down_unicast_demand) as down_unicast_demand,sum(down_bandwidth) as down_bandwidth,sum(down_sum) as down_sum from 9_1_user_table ut " \
                   "where ut.is_LAN = 'LAN' and ut.OLT_IP = '%s' ;" % i['OLT_IP']
            res2 = cli.fetchall(sql2)[0]
            if res1['OLT_IP'] == None:
                # only lan user
                i['up_multiple_user_live'] = res2['up_multiple_user_live']
                i['up_multiple_user_demand'] = res2['up_multiple_user_demand']
                i['up_unicast_live'] = res2['up_unicast_live']
                i['up_unicast_demand'] = res2['up_unicast_demand']
                i['up_bandwidth'] = res2['up_bandwidth']
                i['up_sum'] = res2['up_sum']

                i['down_multiple_user_live'] = 1500
                i['down_multiple_demand'] = res2['down_multiple_demand']
                i['down_unicast_live'] = res2['down_unicast_live']
                i['down_unicast_demand'] = res2['down_unicast_demand']
                i['down_bandwidth'] = res2['down_bandwidth']
                i['down_sum'] = i['down_multiple_user_live'] + i['down_multiple_demand'] + i['down_unicast_live'] + i[
                    'down_unicast_demand'] + i['down_bandwidth']
                print(i)
            elif res2['OLT_IP'] == None:
                # only ftth user
                i['up_multiple_user_live'] = res1['up_multiple_user_live']
                i['up_multiple_user_demand'] = res1['up_multiple_user_demand']
                i['up_unicast_live'] = res1['up_unicast_live']
                i['up_unicast_demand'] = res1['up_unicast_demand']
                i['up_bandwidth'] = res1['up_bandwidth']
                i['up_sum'] = res1['up_sum']

                i['down_multiple_user_live'] = res1['down_multiple_user_live']
                i['down_multiple_demand'] = res1['down_multiple_demand']
                i['down_unicast_live'] = res1['down_unicast_live']
                i['down_unicast_demand'] = res1['down_unicast_demand']
                i['down_bandwidth'] = res1['down_bandwidth']
                i['down_sum'] = i['down_multiple_user_live'] + i['down_multiple_demand'] + i['down_unicast_live'] + i[
                    'down_unicast_demand'] + i['down_bandwidth']
                print(i)
            else:
                # both lan user and ftth user
                i['up_multiple_user_live'] = res1['up_multiple_user_live'] + res2['up_multiple_user_live']
                i['up_multiple_user_demand'] = res1['up_multiple_user_demand'] + res2['up_multiple_user_demand']
                i['up_unicast_live'] = res1['up_unicast_live'] + res2['up_unicast_live']
                i['up_unicast_demand'] = res1['up_unicast_demand'] + res2['up_unicast_demand']
                i['up_bandwidth'] = res1['up_bandwidth'] + res2['up_bandwidth']
                i['up_sum'] = res1['up_sum'] + res2['up_sum']

                i['down_multiple_user_live'] = res1['down_multiple_user_live'] + 1500
                i['down_multiple_demand'] = res1['down_multiple_demand'] + res2['down_multiple_demand']
                i['down_unicast_live'] = res1['down_unicast_live'] + res2['down_unicast_live']
                i['down_unicast_demand'] = res1['down_unicast_demand'] + res2['down_unicast_demand']
                i['down_bandwidth'] = res1['down_bandwidth'] + res2['down_bandwidth']
                i['down_sum'] = res1['down_multiple_user_live'] + 55 + res1['down_multiple_demand'] + res2[
                    'down_multiple_demand'] + res1['down_unicast_live'] + res2['down_unicast_live'] + res1[
                                    'down_unicast_demand'] + res2['down_unicast_demand'] + res1['down_bandwidth'] + \
                                res2[
                                    'down_bandwidth']
                # print(i)
        return res
    return "not match."








def OLT_allow_usernum_10_3_impl():
    sql = "select cu.olt_id,ot.service_slot_count from cu_trunk cu LEFT JOIN cu_olt_device ot on cu.olt_id = ot.OLT_IP " \
          "WHERE cu.equip_type1 = 'olt' and cu.if_olt_up_or_down = 'n' and cu.olt_id <>'10.45.36.19' GROUP BY cu.olt_id ,ot.service_slot_count ;"
    res = cli.fetchall(sql)
    for i in res:
        sql1 = "select count(*) as count from cu_trunk where equip_type1 = 'olt' and if_olt_up_or_down = 'n' and olt_id = '%s' ;"%i['olt_id']
        i['PON_num'] = str(cli.fetchall(sql1)[0]['count'])
        sql2 = "select sum(Link_physical_or_trunk_bandwidth) as max1 from link_name where is_trunk = 'NO' and Network_element_IP = '%s';"%i['olt_id']
        max1 = int((int(cli.fetchall(sql2)[0]['max1'])*1000-1500)/0.84)
        sql3 = "select sum(sr.split_rate) as max2 from cu_trunk cu, split_rate sr where cu.equip_id_link = sr.OS_id and cu.olt_id = '%s';"%i['olt_id']
        max2 = cli.fetchall(sql3)[0]['max2']
        if max1>max2:
            i['max_user_num'] = str(max2)
        else:
            i['max_user_num'] = str(max1)
        sql4 = "select count(*) as count1 from ftth_user_table where OLT_IP = '%s';"%i['olt_id']
        num1 = int(cli.fetchall(sql4)[0]['count1'])
        sql5 = "select count(*) as count2 from lan_user_table where OLT_IP = '%s';"%i['olt_id']
        num = int(cli.fetchall(sql5)[0]['count2'])+num1
        i['now_user_num'] = str(num)
        i['remain_user_'] = str(int(i['max_user_num']) - num)
    return res

def show_ratio_10_4_impl():
    sql = "select * from user_type_and_params where id <4 ;"
    sql1 = "update user_type_and_params SET ratio = '0%' where id = 4"
    cli.execute(sql1)
    res = cli.fetchall(sql)
    sql2 = "select id,user_type,user_speed,ratio from user_type_and_params1 order by user_speed ;"
    res2 = cli.fetchall(sql2)
    tempdic = {}
    tempdic['ratio_modified_table'] = res2
    tempdic['meal_ratio'] = res
    calculate()
    return tempdic

def modified_ratio_10_4_impl(params):
    for i in range(1,4):
        sql = "update user_type_and_params SET ratio = '%s' where id = '%s';"%tuple([params[i-1],i])
        cli.execute(sql)
    calculate()



def cal_meal_case1_10_4_impl(lan_user_number,ftth_user_number,total_bandwidth):
    if lan_user_number == None:
        lan_user_number = 0
    if ftth_user_number == None:
        ftth_user_number = 0
    if total_bandwidth == None:
        total_bandwidth = 0
    sql1 = "select * from user_type_and_params2 where id = 2 ;"
    params = cli.fetchall(sql1)[0]
    templist = []
    templist.append(0)
    templist.append(0)
    templist.append(0)
    templist.append(0)
    templist.append(0.24)
    templist.append(0.24)
    templist.append(0.4) #multiple_live
    templist.append(0.1)
    templist.append(0.4)
    templist.append(0.1)
    templist.append(0.6)
    templist.append(1.6)
    templist[6] = float(params['vedio_user_infiltrate_rate'].split('%')[0]) * 0.01 * float(
        params['vedio_concurrence_rate'].split('%')[0]) * 0.01 * 1.1 * float(
        params['peak_time_live_user_rate'].split('%')[0]) * 0.01 * (
                          float(params['4K_rate'].split('%')[0]) * 0.01 * 50 + float(
                      params['HD_rate'].split('%')[0]) * 0.01 * 8 + float(
                      params['SD_rate'].split('%')[0]) * 0.01 * 2.5)
    templist[8] = templist[6]
    templist[7] = float(params['vedio_user_infiltrate_rate'].split('%')[0]) * 0.01 * float(
        params['vedio_concurrence_rate'].split('%')[0]) * 0.01 * 1.1 * float(
        params['peak_time_demand_user_rate'].split('%')[0]) * 0.01 * params['demand_user_avg_bandwidth']
    templist[9] = templist[7]
    templist[10] = float(params['boardband_concurrence_rate'].split('%')[0]) * 0.01 * params[
        'boardband_service_avg_bandwidth']
    templist[11] = templist[6] + templist[7] + templist[8] + templist[9] + templist[10]
    templist[4] = templist[10] / 4
    templist[5] = templist[0] + templist[1] + templist[2] + templist[3] + templist[4]
    lan_bandwidth = int(lan_user_number)*(templist[7] + templist[8] + templist[9] + templist[10])+1500
    ftth_bandwidth = int(ftth_user_number)*templist[11]
    needed_bandwidth = lan_bandwidth+ftth_bandwidth
    print(lan_bandwidth)
    print(ftth_bandwidth)
    print(needed_bandwidth)
    print(total_bandwidth)
    if float(total_bandwidth)>float(needed_bandwidth):
        return "real bandwidth match requset bandwidth."
    else:
        return "real bandwidth doesn't match requset bandwidth."

def select_user_by_speed_10_4_impl(OLT_IP):
    if OLT_IP==None or OLT_IP == '':
        sql = "select SPEED , count(*) as count from ftth_user_table  where SPEED!='' GROUP BY SPEED ORDER BY SPEED"
    else:
        sql = "select SPEED , count(*) as count from ftth_user_table  where SPEED!='' and OLT_IP='%s' GROUP BY SPEED ORDER BY SPEED" % OLT_IP
    res = cli.fetchall(sql)
    print(res)
    return res

def recommned_meal_case1_10_4_impl(user_num,total_bandwidth):
    if user_num == None or user_num == '':
        user_num = 0
        return "user_number error."
    if total_bandwidth == None or total_bandwidth == '':
        total_bandwidth = 0
        return "total_bandwidth error."
    user_num = int(user_num)
    total_bandwidth = int(total_bandwidth)
    # sql1 = "select * from user_type_and_params;"
    # res1 = cli.fetchall(sql1)
    res1 = ['200M','300M','500M']
    boardband_service_avg_bandwidth = []
    count = 0
    for i in res1:
        boardband_service_avg_bandwidth.append(0)
        sql2 = "select * from user_type_and_params1 where user_speed = '%s';" % i
        res2 = cli.fetchall(sql2)
        for j in res2:
            print(float(j['ratio'].split('%')[0]) * 0.01 * j['peak_rate'] )
            boardband_service_avg_bandwidth[count] += float(j['ratio'].split('%')[0]) * 0.01 * j['peak_rate']
        count+=1
    print(boardband_service_avg_bandwidth)
    needed_bandwidth = []
    count_needed_bandwidth = 0
    for i in boardband_service_avg_bandwidth:
        """取每类套餐的下行总流量计算"""
        sql3 = "update user_type_and_params2 SET boardband_service_avg_bandwidth = '%s' where id = 2;" % i
        cli.execute(sql3)
        sql1 = "select * from user_type_and_params2 where id = 2 ;"
        params = cli.fetchall(sql1)[0]
        templist = []
        templist.append(0)
        templist.append(0)
        templist.append(0)
        templist.append(0)
        templist.append(0.24)
        templist.append(0.24)
        templist.append(0.4)  # multiple_live
        templist.append(0.1)
        templist.append(0.4)
        templist.append(0.1)
        templist.append(0.6)
        templist.append(1.6)
        templist[6] = float(params['vedio_user_infiltrate_rate'].split('%')[0]) * 0.01 * float(
            params['vedio_concurrence_rate'].split('%')[0]) * 0.01 * 1.1 * float(
            params['peak_time_live_user_rate'].split('%')[0]) * 0.01 * (
                              float(params['4K_rate'].split('%')[0]) * 0.01 * 50 + float(
                          params['HD_rate'].split('%')[0]) * 0.01 * 8 + float(
                          params['SD_rate'].split('%')[0]) * 0.01 * 2.5)
        templist[8] = templist[6]
        templist[7] = float(params['vedio_user_infiltrate_rate'].split('%')[0]) * 0.01 * float(
            params['vedio_concurrence_rate'].split('%')[0]) * 0.01 * 1.1 * float(
            params['peak_time_demand_user_rate'].split('%')[0]) * 0.01 * params['demand_user_avg_bandwidth']
        templist[9] = templist[7]
        templist[10] = float(params['boardband_concurrence_rate'].split('%')[0]) * 0.01 * params[
            'boardband_service_avg_bandwidth']
        templist[11] = templist[6] + templist[7] + templist[8] + templist[9] + templist[10]
        templist[4] = templist[10] / 4
        templist[5] = templist[0] + templist[1] + templist[2] + templist[3] + templist[4]
        needed_bandwidth.append(templist[11])
        count_needed_bandwidth+=1
    print(needed_bandwidth)
    """套餐推荐算法"""
    boundary = [needed_bandwidth[0]*user_num,needed_bandwidth[1]*user_num,needed_bandwidth[2]*user_num]
    bandwidth_except_multiple_user_live = total_bandwidth-1500
    if bandwidth_except_multiple_user_live<boundary[0]:
        return "input bandwidth doesn't match user number."
    elif boundary[0]<=bandwidth_except_multiple_user_live<boundary[1]:
        return cal1(needed_bandwidth,bandwidth_except_multiple_user_live,user_num)
    elif boundary[1]<=bandwidth_except_multiple_user_live<boundary[2]:
        return cal1(needed_bandwidth,bandwidth_except_multiple_user_live,user_num)
    elif bandwidth_except_multiple_user_live>=boundary[2]:
        tempdic = {}
        tempdic['200M']=0
        tempdic['300M'] = 0
        tempdic['500M'] = user_num
        return tempdic

def cal1(needed_bandwidth,bandwidth_except_multiple_user_live,user_num):

    user_num_list = [user_num,0,0]
    used_bandwidth = user_num_list[0]*needed_bandwidth[0] + user_num_list[1]*needed_bandwidth[1] + user_num_list[2]*needed_bandwidth[2]
    tempdic = {}
    while(bandwidth_except_multiple_user_live>used_bandwidth):
        if user_num_list[0]!=0:
            if user_num_list[1]==0:
                user_num_list[0]-=1
                user_num_list[1]+=1
                used_bandwidth = user_num_list[0] * needed_bandwidth[0] + user_num_list[1] * needed_bandwidth[1] + \
                                 user_num_list[2] * needed_bandwidth[2]
                if bandwidth_except_multiple_user_live<=used_bandwidth:
                    tempdic['200M'] = user_num_list[0]+1
                    tempdic['300M'] = user_num_list[1]-1
                    tempdic['500M'] = user_num_list[2]
                    return tempdic
            elif user_num_list[1] != 0:
                user_num_list[1] -= 1
                user_num_list[2] += 1
                used_bandwidth = user_num_list[0] * needed_bandwidth[0] + user_num_list[1] * needed_bandwidth[1] + \
                                 user_num_list[2] * needed_bandwidth[2]
                if bandwidth_except_multiple_user_live<=used_bandwidth:
                    tempdic['200M'] = user_num_list[0]
                    tempdic['300M'] = user_num_list[1]+1
                    tempdic['500M'] = user_num_list[2]-1
                    return tempdic
        else:
            tempdic['200M'] = 0
            tempdic['300M'] = user_num_list[1]
            tempdic['500M'] = user_num_list[2]
            return tempdic


def device_ability_11_1_impl():
    res = {}
    sql = "select * from 11_1_PON ;"
    res['PON'] = cli.fetchall(sql)
    sql2 = "select * from 11_1_OLT_up ;"
    res['OLT_UP'] = cli.fetchall(sql2)
    return res


def plan_11_2_impl():
    res = {}
    sql = "select * from 11_2_device ;"
    res['station'] = cli.fetchall(sql)
    sql2 = "select * from 11_2_OLT ;"
    res['OLT'] = cli.fetchall(sql2)
    sql3 = "select * from 11_2_PON_board ;"
    res['board'] = cli.fetchall(sql3)
    sql4 = "select * from 11_2_olt_up ;"
    res['olt_up'] = cli.fetchall(sql4)
    return res

def cut_11_3_impl():
    sql = "select * from 11_3_cut ;"
    return cli.fetchall(sql)

def plan_12_1_impl():
    res = {}
    sql = "select * from 12_1_device ;"
    res['station'] = cli.fetchall(sql)
    sql2 = "select * from 12_1_OLT ;"
    res['OLT'] = cli.fetchall(sql2)
    return res