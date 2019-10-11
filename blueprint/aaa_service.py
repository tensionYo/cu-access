# encoding = utf-8

from db.client import cli
from utils.tools import parse_traffic_rate

import numpy as np


def distribution(data, bins_interval):
    bins = list(range(min(data), max(data) + bins_interval, bins_interval))
    hist = np.histogram(data, bins)
    return hist[0]


def get_top_k_aaa_user(dp, st, dt, k):
    """
    :type dp: str
    :type dt: str
    :type st: str
    :type k: float
    :param dp:
    :param dt:
    :param k:
    :return:
    """
    table_name = "aaa_tianjin_users_tj-{}_all".format(dt)
    res = dict()
    if st:
        count_sql = "select count(*) as cnt from `{}` where department_name = '{}' and station = '{}';".format(
            table_name, dp, st)
        limit = int(cli.fetchone(count_sql)['cnt'] * k)
        ds_list_sql = "SELECT id, upstream, downstream, online_time, department_name, station, OLT_name AS olt_name, " \
                      "PON_board AS pon_board, PON_port AS pon_port, speed, ONU AS onu FROM `{}` " \
                      "where department_name = '{}' and station = '{}' " \
                      "order by downstream desc LIMIT {};".format(table_name, dp, st, limit)
        ds_sum_sql = "select sum(downstream) as s from `{}` where department_name = '{}' and station = '{}';".format(
            table_name,
            dp, st)
        us_list_sql = "SELECT id, upstream, downstream, online_time, department_name, station, OLT_name AS olt_name, " \
                      "PON_board AS pon_board, PON_port AS pon_port, speed, ONU AS onu FROM `{}` " \
                      "where department_name = '{}' and station = '{}' " \
                      "order by upstream desc LIMIT {};".format(table_name, dp, st, limit)
        us_sum_sql = "select sum(upstream) as s from `{}` where department_name = '{}' and station = '{}';".format(
            table_name, dp, st)
    else:
        count_sql = "select count(*) as cnt from `{}` where department_name = '{}';".format(
            table_name, dp)
        limit = int(cli.fetchone(count_sql)['cnt'] * k)
        ds_list_sql = "SELECT id, upstream, downstream, online_time, department_name, station, OLT_name AS olt_name, " \
                      "PON_board AS pon_board, PON_port AS pon_port, speed, ONU AS onu FROM `{}` " \
                      "where department_name = '{}' order by downstream desc LIMIT {};".format(table_name, dp, limit)
        ds_sum_sql = "select sum(downstream) as s from `{}` where department_name = '{}';".format(table_name, dp)
        us_list_sql = "SELECT id, upstream, downstream, online_time, department_name, station, OLT_name AS olt_name, " \
                      "PON_board AS pon_board, PON_port AS pon_port, speed, ONU AS onu FROM `{}` " \
                      "where department_name = '{}' " \
                      "order by upstream desc LIMIT {};".format(table_name, dp, limit)
        us_sum_sql = "select sum(upstream) as s from `{}` where department_name = '{}';".format(table_name, dp)
    s = cli.fetchall(ds_list_sql)
    res['downstream'] = {
        'total_traffic': round(cli.fetchone(ds_sum_sql)['s'], 2),
        'head_traffic': round(sum(map(lambda x: x['downstream'], s)), 2),
        'list': s
    }
    s = cli.fetchall(us_list_sql)
    res['upstream'] = {
        'total_traffic': round(cli.fetchone(us_sum_sql)['s'], 2),
        'head_traffic': round(sum(map(lambda x: x['upstream'], s)), 2),
        'list': s
    }
    return res


def get_pon_port_traffic_statistics(city_name, department_name, interval):
    """
    :type city_name: str,
    :type department_name: str
    :type interval: int
    :param city_name:
    :param department_name:
    :return:
    """
    if city_name and department_name:
        sql = "SELECT input_average_traffic, input_peak_traffic, " \
              "output_average_traffic, output_peak_traffic " \
              "FROM pon_traffic_statistics_csv " \
              "WHERE city_name = '{}' AND department_name = '{}';".format(city_name, department_name)
    elif city_name:
        sql = "SELECT input_average_traffic, input_peak_traffic, " \
              "output_average_traffic, output_peak_traffic " \
              "FROM pon_traffic_statistics_csv " \
              "WHERE city_name = '{}';".format(city_name)
    else:
        sql = ''
    r = cli.fetchall(sql)
    f = {
        'in_avg': map(lambda x: parse_traffic_rate(x['input_average_traffic']), r),
        'in_peak': map(lambda x: parse_traffic_rate(x['input_peak_traffic']), r),
        'out_avg': map(lambda x: parse_traffic_rate(x['output_average_traffic']), r),
        'out_peak': map(lambda x: parse_traffic_rate(x['output_peak_traffic']), r)
    }
    res = {}
    for k, v in f.items():
        res[k] = {
            'y': list(distribution(v, interval))
        }
        res[k]['x'] = range(0, len(res[k]['y']) * interval, interval)
    return res
