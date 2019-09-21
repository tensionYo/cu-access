# -*- coding: utf-8 -*-
from flask import request
from db.client import query_list, query_one
from utils.decorator import json_resp
from utils.tools import all_none


@json_resp
def menu_department():
    """
    :rtype: dict
    :return:
    """
    sql = 'SELECT city_name, department_name FROM sum_tianjin_for_interface GROUP BY city_name, department_name;'
    res = query_list(sql)
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
    sql = 'select department_name, station from sum_tianjin_for_interface ' \
          'where city_name = "{}" and department_name = "{}" ' \
          'GROUP BY city_name, department_name, station;'.format(city_name, department_name)
    res = query_list(sql)
    return dict(success=True, data=map(lambda x: x['station'], res))


@json_resp
def menus_olt(city_name, department_name, station):
    sql = 'select station, OLT_port as olt_name from sum_tianjin_for_interface ' \
          'where city_name = "{}" and department_name = "{}" and station = "{}" ' \
          'GROUP BY city_name, department_name, station, olt_name;'.format(city_name, department_name, station)
    res = query_list(sql)
    return dict(success=True, data=map(lambda x: x['olt_name'], res))


@json_resp
def menus():
    sql = 'SELECT city_name, department_name, station, OLT_port AS olt_name FROM sum_tianjin_for_interface ' \
          'GROUP BY city_name, department_name, station, OLT_port;'
    _res = query_list(sql)
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
        sql = 'SELECT city_name, department_name, station, count(DISTINCT OLT_port) AS olt_count ' \
              'FROM sum_tianjin_for_interface where city_name = "{}" AND department_name = "{}" AND station = "{}" ' \
              'GROUP BY city_name, department_name, station;'.format(city.encode('utf-8'),
                                                                     department.encode('utf-8'),
                                                                     station)
        res = query_one(sql)
    elif department and city:
        sql = 'SELECT city_name, department_name, count(DISTINCT OLT_port) AS olt_count ' \
              'FROM sum_tianjin_for_interface where city_name = "{}" AND department_name = "{}" ' \
              'GROUP BY city_name, department_name;'.format(city.encode('utf-8'),
                                                            department.encode('utf-8'))
        res = query_one(sql)
    elif city:
        sql = 'SELECT city_name, count(DISTINCT OLT_port) AS olt_count ' \
              'FROM sum_tianjin_for_interface where city_name = "{}" ' \
              'GROUP BY city_name;'.format(city.encode('utf-8'))
        res = query_one(sql)
    else:
        return dict(success=False, msg='query parameter invalid.')
    # if label == 'city':
    #     sql = 'SELECT city_name, count(DISTINCT OLT_port) AS olt_count ' \
    #           'FROM sum_tianjin_for_interface GROUP BY city_name;'
    # elif label == 'department':
    #     sql = 'SELECT city_name, department_name, count(DISTINCT OLT_port) AS olt_count ' \
    #           'FROM sum_tianjin_for_interface GROUP BY city_name, department_name;'
    # elif label == 'station':
    #     sql = 'SELECT city_name, department_name, station, count(DISTINCT OLT_port) AS olt_count ' \
    #           'FROM sum_tianjin_for_interface GROUP BY city_name, department_name, station;'
    # else:
    #     return []
    # res = query_list(sql)
    return dict(success=True, data=res)


@json_resp
def olt_manufacturer_count(label):
    city = request.args.get('city', None)
    department = request.args.get('department', None)
    station = request.args.get('station', None)
    if all_none([city, department, station]):
        return dict(success=False, msg='query parameter invalid.')

    if station and department and city:
        sql = 'SELECT city_name, department_name, station, substring_index(substring_index(OLT_port, ' \
              '\'_\', 2), \'_\', -1) AS brand, count(DISTINCT OLT_port) AS olt_count ' \
              'FROM sum_tianjin_for_interface where city_name = "{}" and department_name = "{}" and station = "{}" ' \
              'GROUP BY city_name, department_name, station, brand;'.format(city.encode('utf-8'),
                                                                            department.encode('utf-8'),
                                                                            station)
        res = query_list(sql)
    elif department and city:
        sql = 'SELECT city_name, department_name, ' \
              'substring_index(substring_index(OLT_port, \'_\', 2), \'_\', -1) AS brand, ' \
              'count(DISTINCT OLT_port) AS olt_count ' \
              'FROM sum_tianjin_for_interface WHERE city_name = "{}" AND department_name = "{}" ' \
              'GROUP BY city_name, department_name, brand;'.format(city.encode('utf-8'),
                                                                   department.encode('utf-8'))
        res = query_list(sql)
    elif city:
        sql = 'SELECT city_name, substring_index(substring_index(OLT_port, \'_\', 2), \'_\', -1) AS brand, ' \
              'count(DISTINCT OLT_port) AS olt_count FROM sum_tianjin_for_interface GROUP BY city_name, brand;' \
            .format(city.encode('utf-8'))
        res = query_list(sql)
    else:
        res = {}
    # sql = {
    #     'city': 'SELECT city_name, substring_index(substring_index(OLT_port, \'_\', 2), \'_\', -1) AS brand, '
    #             'count(DISTINCT OLT_port) AS olt_count FROM sum_tianjin_for_interface GROUP BY city_name, brand;',
    #     'department': 'SELECT city_name, department_name, '
    #                   'substring_index(substring_index(OLT_port, \'_\', 2), \'_\', -1) AS brand, '
    #                   'count(DISTINCT OLT_port) AS olt_count '
    #                   'FROM sum_tianjin_for_interface GROUP BY city_name, department_name, brand;',
    #     'station': 'SELECT city_name, department_name, station, substring_index(substring_index(OLT_port, '
    #                '\'_\', 2), \'_\', -1) AS brand, count(DISTINCT OLT_port) AS olt_count '
    #                'FROM sum_tianjin_for_interface GROUP BY city_name, department_name, station, brand;'
    # }
    # VENDOR_MAP = {
    #     'HW': u'华为',
    #     'ZX': u'中兴',
    #     'FH': u'烽火'
    # }
    # res = query_list(sql[label]) if label in sql else []
    return dict(success=True, data=res)


@json_resp
def olt_user_count(label):
    city = request.args.get('city', None)
    department = request.args.get('department', None)
    station = request.args.get('station', None)
    if all_none([city, department, station]):
        return dict(success=False, msg='query parameter invalid.')

    if station and department and city:
        sql = 'SELECT city_name, department_name, station, count(*) AS user_count ' \
              'FROM sum_tianjin_for_interface WHERE city_name = "{}" and department_name = "{}" and station = "{}" ' \
              'GROUP BY city_name, department_name, station, OLT_port;'.format(city.encode('utf-8'),
                                                                               department.encode('utf-8'),
                                                                               station)
        res = query_list(sql)
    elif department and city:
        sql = 'SELECT city_name, department_name, count(*) AS user_count ' \
              'FROM sum_tianjin_for_interface where city_name = "{}" and department_name = "{}" ' \
              'GROUP BY city_name, department_name, OLT_port;'.format(city.encode('utf-8'),
                                                                      department.encode('utf-8'))
        res = query_list(sql)
    elif city:
        sql = 'SELECT city_name, count(*) AS user_count ' \
              'FROM sum_tianjin_for_interface where city_name = "{}" ' \
              'GROUP BY city_name, OLT_port;'.format(city.encode('utf-8'))
        res = query_list(sql)
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
    # sql = {
    #     'city': 'SELECT city_name, count(*) AS user_count '
    #             'FROM sum_tianjin_for_interface GROUP BY city_name;',
    #     'department': 'SELECT city_name, department_name, count(*) AS user_count '
    #                   'FROM sum_tianjin_for_interface GROUP BY city_name, department_name;',
    #     'station': 'SELECT city_name, department_name, station, count(*) AS user_count '
    #                'FROM sum_tianjin_for_interface GROUP BY city_name, department_name, station;'
    # }
    # res = query_list(sql[label]) if label in sql else []
    return dict(success=True, data=resp)


@json_resp
def olt_vendor_branch_distribution(label):
    city = request.args.get('city', None)
    department = request.args.get('department', None)
    station = request.args.get('station', None)
    if all_none([city, department, station]):
        return dict(success=False, msg='query parameter invalid.')

    if station and department and city:
        sql = 'SELECT pon.manufacturer         AS brand, ' \
              '       pon_users.city_name      AS city_name, ' \
              '       pon_users.department_name, ' \
              '       pon_users.station, ' \
              '       pon.device_model         AS model, ' \
              '       count(DISTINCT OLT_port) AS olt_count ' \
              'FROM sum_tianjin_for_interface AS pon_users ' \
              '       INNER JOIN relay_circuit_mapping AS mapping ' \
              '        ON mapping.z_end_name = pon_users.OLT_port ' \
              '       INNER JOIN cu.pon_traffic_statistics_csv AS pon ON pon.ip = mapping.ip ' \
              'WHERE pon_users.city_name = "{}" and pon_users.department_name = "{}" and pon_users.station = "{}" ' \
              'GROUP BY pon.manufacturer, city_name, department_name, station, model;'.format(city.encode('utf-8'),
                                                                                              department.encode(
                                                                                                  'utf-8'),
                                                                                              station)
        res = query_list(sql)
    elif department and city:
        sql = 'SELECT pon.manufacturer         AS brand, ' \
              '       pon_users.city_name      AS city_name, ' \
              '       pon_users.department_name, ' \
              '       pon.device_model         AS model, ' \
              '       count(DISTINCT OLT_port) AS olt_count ' \
              'FROM sum_tianjin_for_interface AS pon_users ' \
              '       INNER JOIN relay_circuit_mapping AS mapping ' \
              '        ON mapping.z_end_name = pon_users.OLT_port ' \
              '       INNER JOIN cu.pon_traffic_statistics_csv AS pon ON pon.ip = mapping.ip ' \
              'WHERE pon_users.city_name = "{}" and pon_users.department_name = "{}" ' \
              'GROUP BY pon.manufacturer, city_name, department_name, model;'.format(city.encode('utf-8'),
                                                                                     department.encode('utf-8'))
        res = query_list(sql)
    elif city:
        sql = 'SELECT pon.manufacturer         AS brand, ' \
              '       pon_users.city_name      AS city_name, ' \
              '       pon.device_model         AS model, ' \
              '       count(DISTINCT OLT_port) AS olt_count ' \
              'FROM sum_tianjin_for_interface AS pon_users ' \
              '       INNER JOIN relay_circuit_mapping AS mapping ' \
              '        ON mapping.z_end_name = pon_users.OLT_port ' \
              '       INNER JOIN cu.pon_traffic_statistics_csv AS pon ON pon.ip = mapping.ip ' \
              'WHERE pon_users.city_name = "{}" ' \
              'GROUP BY pon.manufacturer, city_name, model;'.format(city.encode('utf-8'))
        res = query_list(sql)
    else:
        res = {}

    # sql = {
    #     'city': 'SELECT pon.manufacturer         AS brand, '
    #             '       pon_users.city_name      AS city_name, '
    #             '       pon.device_model         AS model, '
    #             '       count(DISTINCT OLT_port) AS olt_count '
    #             'FROM pon_traffic_statistics_csv AS pon '
    #             '       INNER JOIN relay_circuit_mapping AS mapping ON pon.ip = mapping.ip '
    #             '       INNER JOIN sum_tianjin_for_interface AS pon_users ON mapping.z_end_name = pon_users.OLT_port '
    #             'GROUP BY pon.manufacturer, city_name, model;',
    #     'department': 'SELECT pon.manufacturer         AS brand, '
    #                   '       pon_users.city_name      AS city_name, '
    #                   '       pon_users.department_name, '
    #                   '       pon.device_model         AS model, '
    #                   '       count(DISTINCT OLT_port) AS olt_count '
    #                   'FROM pon_traffic_statistics_csv AS pon '
    #                   '       INNER JOIN relay_circuit_mapping AS mapping ON pon.ip = mapping.ip '
    #                   '       INNER JOIN sum_tianjin_for_interface AS pon_users '
    #                   'ON mapping.z_end_name = pon_users.OLT_port '
    #                   'GROUP BY pon.manufacturer, city_name, department_name, model;',
    #
    #     'station': 'SELECT pon.manufacturer         AS brand, '
    #                '       pon_users.city_name      AS city_name, '
    #                '       pon_users.department_name, '
    #                '       pon_users.station, '
    #                '       pon.device_model         AS model, '
    #                '       count(DISTINCT OLT_port) AS olt_count '
    #                'FROM pon_traffic_statistics_csv AS pon '
    #                '       INNER JOIN relay_circuit_mapping AS mapping ON pon.ip = mapping.ip '
    #                '       INNER JOIN sum_tianjin_for_interface AS pon_users '
    #                'ON mapping.z_end_name = pon_users.OLT_port '
    #                'GROUP BY pon.manufacturer, city_name, department_name, station, model;'
    # }
    # res = query_list(sql[label]) if label in sql else []
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
        sql = 'SELECT csv.city_name, sub_company AS department_name, station, count(port) AS pon_port_count ' \
              'FROM pon_traffic_statistics_csv AS csv ' \
              'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip ' \
              'where csv.city_name = "{}" and department_name = "{}" and station = "{}" and mapping.z_end_name = "{}" ' \
              'GROUP BY csv.city_name, department_name, station;'.format(city.encode('utf-8'),
                                                                         department.encode('utf-8'),
                                                                         station,
                                                                         olt)
        res = query_one(sql)
    elif station and department and city:
        sql = 'SELECT csv.city_name, sub_company AS department_name, station, count(port) AS pon_port_count ' \
              'FROM pon_traffic_statistics_csv AS csv ' \
              'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip ' \
              'where csv.city_name = "{}" and sub_company = "{}" and station = "{}" ' \
              'GROUP BY csv.city_name, department_name, station;'.format(city.encode('utf-8'),
                                                                         department.encode('utf-8'),
                                                                         station)
        res = query_one(sql)
    elif department and city:
        sql = 'SELECT csv.city_name, sub_company AS department_name, count(port) AS pon_port_count ' \
              'FROM pon_traffic_statistics_csv AS csv ' \
              'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip ' \
              'where csv.city_name = "{}" and sub_company = "{}" ' \
              'GROUP BY csv.city_name, department_name;'.format(city.encode('utf-8'),
                                                                department.encode('utf-8'))
        res = query_one(sql)
    elif city:
        sql = 'SELECT csv.city_name, count(port) AS pon_port_count ' \
              'FROM pon_traffic_statistics_csv AS csv ' \
              'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip ' \
              'where csv.city_name = "{}" ' \
              'GROUP BY csv.city_name;'.format(city.encode('utf-8'))
        res = query_one(sql)
    else:
        res = {}
    # sql = {
    #     'city': 'SELECT city_name, count(port) AS pon_port_count '
    #             'FROM pon_traffic_statistics_csv AS csv '
    #             'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip '
    #             'GROUP BY city_name;',
    #     'department': 'SELECT city_name, sub_company AS department_name, count(port) AS pon_port_count '
    #                   'FROM pon_traffic_statistics_csv AS csv '
    #                   'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip '
    #                   'GROUP BY city_name, department_name;',
    #     'station': 'SELECT city_name, sub_company AS department_name, station, count(port) AS pon_port_count '
    #                'FROM pon_traffic_statistics_csv AS csv '
    #                'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip '
    #                'GROUP BY city_name, department_name, station;',
    # }
    # res = query_list(sql[label]) if label in sql else []
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
        sql = 'SELECT ' \
              'csv.city_name, ' \
              'sub_company                                             AS department_name, ' \
              'mapping.station, mapping.z_end_name AS olt_name, ' \
              'sum(if(input_peak_traffic = \'0.00Mb/s\' ' \
              'AND input_average_traffic = \'0.00Mb/s\' ' \
              'AND output_peak_traffic = \'0.00Mb/s\' ' \
              'AND output_average_traffic = \'0.00Mb/s\', 1, 0))  AS idle_port_count, ' \
              'sum(if(input_peak_traffic <> \'0.00Mb/s\' ' \
              'OR input_average_traffic <> \'0.00Mb/s\' ' \
              'OR output_peak_traffic <> \'0.00Mb/s\' ' \
              'OR output_average_traffic <> \'0.00Mb/s\', 1, 0)) AS used_port_count ' \
              'FROM pon_traffic_statistics_csv AS csv ' \
              'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip ' \
              'WHERE csv.city_name = "{}" AND sub_company = "{}" AND station = "{}" AND z_end_name = "{}" ' \
              'GROUP BY csv.city_name, sub_company, mapping.station, olt_name;'.format(city.encode('utf-8'),
                                                                                       department.encode('utf-8'),
                                                                                       station, olt)
        res = query_one(sql)
    elif station and department and city:
        sql = 'SELECT ' \
              'csv.city_name, ' \
              'sub_company                                             AS department_name, ' \
              'mapping.station, ' \
              'sum(if(input_peak_traffic = \'0.00Mb/s\' ' \
              'AND input_average_traffic = \'0.00Mb/s\' ' \
              'AND output_peak_traffic = \'0.00Mb/s\' ' \
              'AND output_average_traffic = \'0.00Mb/s\', 1, 0))  AS idle_port_count, ' \
              'sum(if(input_peak_traffic <> \'0.00Mb/s\' ' \
              'OR input_average_traffic <> \'0.00Mb/s\' ' \
              'OR output_peak_traffic <> \'0.00Mb/s\' ' \
              'OR output_average_traffic <> \'0.00Mb/s\', 1, 0)) AS used_port_count ' \
              'FROM pon_traffic_statistics_csv AS csv ' \
              'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip ' \
              'where csv.city_name = "{}" and sub_company = "{}" and station = "{}" ' \
              'GROUP BY csv.city_name, sub_company, mapping.station;'.format(city.encode('utf-8'),
                                                                             department.encode('utf-8'),
                                                                             station)
        res = query_one(sql)
    elif department and city:
        sql = 'SELECT city_name, sub_company AS department_name, ' \
              'sum(if(input_peak_traffic = \'0.00Mb/s\' ' \
              'AND input_average_traffic = \'0.00Mb/s\' ' \
              'AND output_peak_traffic = \'0.00Mb/s\' ' \
              'AND output_average_traffic = \'0.00Mb/s\', 1, 0)) AS idle_port_count, ' \
              'sum(if(input_peak_traffic <> \'0.00Mb/s\' ' \
              'OR input_average_traffic <> \'0.00Mb/s\' ' \
              'OR output_peak_traffic <> \'0.00Mb/s\' ' \
              'OR output_average_traffic <> \'0.00Mb/s\', 1, 0)) AS used_port_count ' \
              'FROM pon_traffic_statistics_csv ' \
              'where city_name = "{}" and sub_company = "{}" ' \
              'GROUP BY city_name, department_name;'.format(city.encode('utf-8'),
                                                            department.encode('utf-8'))
        res = query_one(sql)
    elif city:
        sql = 'SELECT city_name, sum(if(input_peak_traffic = \'0.00Mb/s\' ' \
              'AND input_average_traffic = \'0.00Mb/s\' ' \
              'AND output_peak_traffic = \'0.00Mb/s\' ' \
              'AND output_average_traffic = \'0.00Mb/s\', 1, 0)) AS idle_port_count, ' \
              'sum(if(input_peak_traffic <> \'0.00Mb/s\' ' \
              'OR input_average_traffic <> \'0.00Mb/s\' ' \
              'OR output_peak_traffic <> \'0.00Mb/s\' ' \
              'OR output_average_traffic <> \'0.00Mb/s\', 1, 0)) AS used_port_count ' \
              'FROM pon_traffic_statistics_csv ' \
              'where city_name = "{}" ' \
              'GROUP BY city_name;'.format(city.encode('utf-8'))
        res = query_one(sql)
    else:
        res = {}
    # sql = {
    #     'city': 'SELECT city_name, sum(if(input_peak_traffic = \'0.00Mb/s\' '
    #             'AND input_average_traffic = \'0.00Mb/s\' '
    #             'AND output_peak_traffic = \'0.00Mb/s\' '
    #             'AND output_average_traffic = \'0.00Mb/s\', 1, 0)) AS idle_port_count, '
    #             'sum(if(input_peak_traffic <> \'0.00Mb/s\' '
    #             'OR input_average_traffic <> \'0.00Mb/s\' '
    #             'OR output_peak_traffic <> \'0.00Mb/s\' '
    #             'OR output_average_traffic <> \'0.00Mb/s\', 1, 0)) AS used_port_count '
    #             'FROM pon_traffic_statistics_csv '
    #             'GROUP BY city_name;',
    #     'department': 'SELECT city_name, sub_company AS department_name, '
    #                   'sum(if(input_peak_traffic = \'0.00Mb/s\' '
    #                   'AND input_average_traffic = \'0.00Mb/s\' '
    #                   'AND output_peak_traffic = \'0.00Mb/s\' '
    #                   'AND output_average_traffic = \'0.00Mb/s\', 1, 0)) AS idle_port_count, '
    #                   'sum(if(input_peak_traffic <> \'0.00Mb/s\' '
    #                   'OR input_average_traffic <> \'0.00Mb/s\' '
    #                   'OR output_peak_traffic <> \'0.00Mb/s\' '
    #                   'OR output_average_traffic <> \'0.00Mb/s\', 1, 0)) AS used_port_count '
    #                   'FROM pon_traffic_statistics_csv '
    #                   'GROUP BY city_name, department_name;',
    #     'station': 'SELECT '
    #                'csv.city_name, '
    #                'sub_company                                             AS department_name, '
    #                'mapping.station, '
    #                'sum(if(input_peak_traffic = \'0.00Mb/s\' '
    #                'AND input_average_traffic = \'0.00Mb/s\' '
    #                'AND output_peak_traffic = \'0.00Mb/s\' '
    #                'AND output_average_traffic = \'0.00Mb/s\', 1, 0))  AS idle_port_count, '
    #                'sum(if(input_peak_traffic <> \'0.00Mb/s\' '
    #                'OR input_average_traffic <> \'0.00Mb/s\' '
    #                'OR output_peak_traffic <> \'0.00Mb/s\' '
    #                'OR output_average_traffic <> \'0.00Mb/s\', 1, 0)) AS used_port_count '
    #                'FROM pon_traffic_statistics_csv AS csv '
    #                'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip '
    #                'GROUP BY csv.city_name, sub_company, mapping.station;',
    #     'olt': 'SELECT '
    #            'csv.city_name, '
    #            'sub_company                                             AS department_name, '
    #            'mapping.station, mapping.z_end_name AS olt_name, '
    #            'sum(if(input_peak_traffic = \'0.00Mb/s\' '
    #            'AND input_average_traffic = \'0.00Mb/s\' '
    #            'AND output_peak_traffic = \'0.00Mb/s\' '
    #            'AND output_average_traffic = \'0.00Mb/s\', 1, 0))  AS idle_port_count, '
    #            'sum(if(input_peak_traffic <> \'0.00Mb/s\' '
    #            'OR input_average_traffic <> \'0.00Mb/s\' '
    #            'OR output_peak_traffic <> \'0.00Mb/s\' '
    #            'OR output_average_traffic <> \'0.00Mb/s\', 1, 0)) AS used_port_count '
    #            'FROM pon_traffic_statistics_csv AS csv '
    #            'INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip '
    #            'GROUP BY csv.city_name, sub_company, mapping.station, olt_name;'
    # }
    # res = query_list(sql[label]) if label in sql else {}
    # for i in res:
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
        res = query_one(sql)
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
              "where x.city_name = \"{}\" and x.department_name = \"{}\" and x.station = \"{}\" " \
              "GROUP BY city_name, x.department_name, x.station;".format(city.encode('utf-8'),
                                                                         department.encode('utf-8'),
                                                                         station)
        res = query_one(sql)
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
              "where x.city_name = \"{}\" and x.department_name = \"{}\" " \
              "GROUP BY city_name, x.department_name;".format(city.encode('utf-8'),
                                                              department.encode('utf-8'))
        res = query_one(sql)
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
              "where x.city_name = \"{}\" " \
              "GROUP BY city_name;".format(city.encode('utf-8'))
        res = query_one(sql)
    else:
        res = {}
    # sql = {
    #     'city': "SELECT x.city_name, "
    #             "sum(device.service_slot_count) AS total_service_slot_count, "
    #             "sum(x.used_pon_board_count)    AS used_service_slot_count "
    #             "FROM ("
    #             "SELECT itf.city_name, "
    #             "IF(csv.device_model = 'C220v1.2', 'ZXA10 C220', "
    #             "IF(csv.device_model IN ('C300v1.3', 'C300v1.0'), 'ZXA10 C300',"
    #             "csv.device_model))            AS device_model,"
    #             "COUNT(DISTINCT itf.pon_board_number) AS used_pon_board_count "
    #             "FROM sum_tianjin_for_interface AS itf "
    #             "INNER JOIN relay_circuit_mapping AS mapping ON mapping.z_end_name = itf.OLT_port "
    #             "INNER JOIN pon_traffic_statistics_csv AS csv ON csv.ip = mapping.ip "
    #             "GROUP BY city_name, itf.OLT_port, csv.device_model) AS x "
    #             "INNER JOIN olt_device AS device ON x.device_model = device.olt_model "
    #             "GROUP BY city_name;",
    #     'department': "SELECT x.city_name, x.department_name, "
    #                   "sum(device.service_slot_count) AS total_service_slot_count, "
    #                   "sum(x.used_pon_board_count)    AS used_service_slot_count "
    #                   "FROM ("
    #                   "SELECT itf.city_name, itf.department_name, "
    #                   "IF(csv.device_model = 'C220v1.2', 'ZXA10 C220', "
    #                   "IF(csv.device_model IN ('C300v1.3', 'C300v1.0'), 'ZXA10 C300',"
    #                   "csv.device_model))            AS device_model,"
    #                   "COUNT(DISTINCT itf.pon_board_number) AS used_pon_board_count "
    #                   "FROM sum_tianjin_for_interface AS itf "
    #                   "INNER JOIN relay_circuit_mapping AS mapping ON mapping.z_end_name = itf.OLT_port "
    #                   "INNER JOIN pon_traffic_statistics_csv AS csv ON csv.ip = mapping.ip "
    #                   "GROUP BY city_name, itf.department_name, itf.OLT_port, csv.device_model) AS x "
    #                   "INNER JOIN olt_device AS device ON x.device_model = device.olt_model "
    #                   "GROUP BY city_name, x.department_name;",
    #     'station': "SELECT x.city_name, x.department_name, x.station, "
    #                "sum(device.service_slot_count) AS total_service_slot_count, "
    #                "sum(x.used_pon_board_count)    AS used_service_slot_count "
    #                "FROM ("
    #                "SELECT itf.city_name, itf.department_name, itf.station, "
    #                "IF(csv.device_model = 'C220v1.2', 'ZXA10 C220', "
    #                "IF(csv.device_model IN ('C300v1.3', 'C300v1.0'), 'ZXA10 C300',"
    #                "csv.device_model))            AS device_model,"
    #                "COUNT(DISTINCT itf.pon_board_number) AS used_pon_board_count "
    #                "FROM sum_tianjin_for_interface AS itf "
    #                "INNER JOIN relay_circuit_mapping AS mapping ON mapping.z_end_name = itf.OLT_port "
    #                "INNER JOIN pon_traffic_statistics_csv AS csv ON csv.ip = mapping.ip "
    #                "GROUP BY city_name, itf.department_name, itf.station, itf.OLT_port, csv.device_model) AS x "
    #                "INNER JOIN olt_device AS device ON x.device_model = device.olt_model "
    #                "GROUP BY city_name, x.department_name, x.station;"
    # }
    # res = query_list(sql[label]) if label in sql else {}
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
        res = query_one(sql)
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
        res = query_one(sql)
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
        res = query_one(sql)
    elif city:
        sql = "SELECT csv.city_name, " \
              "sum((if(bandwidth IN ('1G', '1.25G', '2.5G', NULL), 1, 0))) AS `1GE_count`, " \
              "sum(if(bandwidth = '10G', 1, 0))                            AS `10GE_count` " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' " \
              "GROUP BY csv.city_name;".format(city.encode('utf-8'))
        res = query_one(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
    elif city:
        sql = "SELECT csv.city_name, manufacturer, " \
              "sum((if(bandwidth IN ('1G', '1.25G', '2.5G', NULL), 1, 0))) AS `1GE_count`, " \
              "sum(if(bandwidth = '10G', 1, 0))                            AS `10GE_count` " \
              "FROM pon_traffic_statistics_csv AS csv " \
              "INNER JOIN relay_circuit_mapping AS mapping ON mapping.ip = csv.ip " \
              "where csv.city_name = '{}' " \
              "GROUP BY csv.city_name, manufacturer;".format(city.encode('utf-8'))
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
    elif department and city:
        sql = "SELECT " \
              "package_speed, " \
              "count(package_speed) AS cnt, " \
              "sum(if(is_iptv_user = '是', 1, 0)) AS iptv_cnt " \
              "FROM sum_tianjin_for_interface " \
              "where city_name = '{}' and department_name = '{}' " \
              "GROUP BY package_speed;".format(city.encode('utf-8'),
                                               department.encode('utf-8'))
        res = query_list(sql)
    elif city:
        sql = "SELECT " \
              "package_speed, " \
              "count(package_speed) AS cnt, " \
              "sum(if(is_iptv_user = '是', 1, 0)) AS iptv_cnt " \
              "FROM sum_tianjin_for_interface " \
              "where city_name = '{}' " \
              "GROUP BY package_speed;".format(city.encode('utf-8'))
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
    elif city:
        sql = "select bandwidth, sum(uplink_port_count) as cnt from(" \
              "SELECT bandwidth, " \
              "count(DISTINCT port) as uplink_port_count " \
              "FROM uplink_traffic_statistics_csv as csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "WHERE mapping.city_name = '{}' " \
              "GROUP BY bandwidth, csv.ip) as x " \
              "group by bandwidth;".format(city.encode('utf-8'))
        res = query_list(sql)
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
        res = query_list(sql)
    elif department and city:
        sql = "SELECT bandwidth " \
              "FROM uplink_traffic_statistics_csv as csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "where mapping.city_name = '{}' and csv.department_name = '{}' " \
              "GROUP BY bandwidth, csv.ip;".format(city.encode('utf-8'),
                                                   department.encode('utf-8'))
        res = query_list(sql)
    elif city:
        sql = "SELECT bandwidth " \
              "FROM uplink_traffic_statistics_csv as csv " \
              "INNER JOIN relay_circuit_mapping as mapping on mapping.ip = csv.ip " \
              "where mapping.city_name = '{}' " \
              "GROUP BY bandwidth, csv.ip;".format(city.encode('utf-8'))
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
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
        res = query_list(sql)
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
            if 0 <= i['total_input_traffic'] < 500:
                resp['0-500Mbps'] += 1
            elif 500 <= i['total_input_traffic'] < 1000:
                resp['500-1000Mbps'] += 1
            elif 1000 <= i['total_input_traffic'] < 15000:
                resp['1000-1500Mbps'] += 1
            elif 1500 <= i['total_input_traffic'] < 2000:
                resp['1500-2000Mbps'] += 1
            else:
                resp['2000Mbps+'] += 1
    return dict(success=True, data=resp)


@json_resp
def olt_info(olt_name):
    # TODO
    if not olt_name:
        return dict(success=False, msg='query parameters invalid.')
