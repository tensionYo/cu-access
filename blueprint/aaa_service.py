# encoding=utf-8

from db.client import cli
from utils.tools import parse_traffic_rate
from itertools import groupby
from datetime import date

import numpy as np

TREND_K = 0.1


class Trend:
    INCREASE = 1
    STABLE = 2
    DECREASE = 3

    def __init__(self):
        raise NotImplemented()

    @staticmethod
    def to_str(trend):
        if trend == Trend.STABLE:
            return 'STABLE'
        elif trend == Trend.INCREASE:
            return 'INCREASE'
        elif trend == Trend.DECREASE:
            return 'DECREASE'
        else:
            return 'INVALID'


def check_trend(k):
    """
    :type k: float
    :param k:
    :return:
    """
    if -TREND_K <= k <= TREND_K:
        return Trend.STABLE
    elif k > TREND_K:
        return Trend.INCREASE
    else:
        return Trend.DECREASE


def build_trend_line(k, b, x_list):
    """
    :type k: float
    :type b: float
    :type x_list: list[float]
    :param k:
    :param b:
    :param x_list:
    :return:
    """
    x1, x2 = min(x_list), max(x_list)
    y1, y2 = round(k * x1 + b, 2), round(k * x2 + b, 2)
    return {
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2
    }


def distribution(data, bins_interval):
    bins = list(range(min(data), max(data) + bins_interval, bins_interval))
    hist = np.histogram(data, bins)
    return hist[0]


def linear_fit(x, y):
    x_data = x
    y_data = y
    poly = np.polyfit(x_data, y_data, deg=1)
    return poly[0], poly[1]


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


def get_pon_trend(city_name, department_name, station, olt_name, tag):
    """
    :type city_name: str
    :type department_name: str
    :type station: str
    :type olt_name: str
    :param city_name:
    :param department_name:
    :param station:
    :param olt_name:
    :return:
    """
    if city_name and department_name and station and olt_name:
        sql = "SELECT department_name, station, olt_name, input_avg, input_peak, " \
              "output_avg, output_peak, pon_board, pon_port, date FROM pon_traffic_time_line " \
              "WHERE department_name = '{}' " \
              "AND station = '{}' " \
              "AND olt_name = '{}'" \
              "ORDER BY department_name, station, olt_name, pon_board, pon_port, date;".format(department_name,
                                                                                               station,
                                                                                               olt_name)
    elif city_name and department_name and station:
        sql = "SELECT department_name, station, olt_name, input_avg, input_peak, " \
              "output_avg, output_peak, pon_board, pon_port, date FROM pon_traffic_time_line " \
              "WHERE department_name = '{}' " \
              "AND station = '{}'" \
              "ORDER BY department_name, station, olt_name, pon_board, pon_port, date;".format(department_name, station)
    elif city_name and department_name:
        sql = "SELECT department_name, station, olt_name, input_avg, input_peak, " \
              "output_avg, output_peak, pon_board, pon_port, date FROM pon_traffic_time_line " \
              "WHERE department_name = '{}'" \
              "ORDER BY department_name, station, olt_name, pon_board, pon_port, date;".format(department_name)
    else:
        return dict(success=False, msg='invalid parameters.')
    r = cli.fetchall(sql)
    z = groupby(r, lambda e: e['department_name'])
    res = []
    for department, stations in z:
        for station, olts in groupby(stations, lambda e: e['station']):
            for olt, boards in groupby(olts, lambda e: e['olt_name']):
                for board, ports in groupby(boards, lambda e: e['pon_board']):
                    for p, records in groupby(ports, lambda e: e['pon_port']):
                        rs = list(records)
                        # x = map(lambda e: e['date'], p)
                        x = [i for i in range(1, len(rs) + 1)]
                        y = map(lambda e: e['{}_avg'.format(tag)], rs)
                        k, b = linear_fit(x, y)
                        trend = check_trend(k)
                        tl = build_trend_line(k, b, x)
                        tl.update({'x1': date.isoformat(rs[0]['date']), 'x2': date.isoformat(rs[-1]['date'])})
                        m = {
                            'department': department,
                            'station': station,
                            'olt': olt,
                            'pon_board': board,
                            'pon_port': p,
                            'type': Trend.to_str(trend),
                            'traffic_tag': tag,
                            'samples': {
                                'x': map(lambda e: date.isoformat(e['date']), rs),
                                'avg': y,
                                'peak': map(lambda e: e['{}_peak'.format(tag)], rs)
                            },
                            'trend_line': tl
                        }
                        res.append(m)
    return res


if __name__ == '__main__':
    r = get_pon_trend('tianjin', '南开分公司', 'NKKYD', 'NKKYD_HW_OLT02', 'input')
    print r
