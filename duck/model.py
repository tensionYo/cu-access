# encoding=utf-8
from db.client import query_one, query_list

parse_rate = lambda x: float(x.rstrip('%'))


def add_leading_zero(n):
    if isinstance(n, (int, str)):
        n = int(n)
        return '%s' % n if n > 9 else '0%s' % n
    raise TypeError('parameter should be in type of int or str, but get {}'.format(type(n)))


def get_pon_status(olt, pon_board_number):
    return get_pon_port_usage_rate(olt, pon_board_number)


def get_pon_port_usage_rate(olt, pon_board_number):
    sql = 'SELECT input_peak_usage_rate, input_average_usage_rate, ' \
          'output_peak_usage_rate, output_average_usage_rate, ' \
          'pon_board_number, pon_port_number ' \
          'FROM pon_traffic_statistics_csv ' \
          'WHERE olt_name = "{}" AND pon_board_number = {};'.format(olt, pon_board_number)
    res = query_list(sql)
    for r in res:
        for k in ['input_peak_usage_rate', 'input_average_usage_rate', 'output_peak_usage_rate',
                  'output_average_usage_rate']:
            r[k] = parse_rate(r[k])
    return res


def get_pon_users_count(olt, pon_board_number):
    sql = 'SELECT olt_name, pon_board, pon_port, ' \
          'COUNT(*) AS user_count FROM new_tianjin_users ' \
          'WHERE olt_name = "{}" AND pon_board = "{}" ' \
          'GROUP BY olt_name, pon_board, pon_port;'.format(olt, add_leading_zero(pon_board_number))
    print sql
    res = query_list(sql)
    return res


if __name__ == '__main__':
    r = get_pon_users_count('2HDHM_HW_OLT01', 2)
    print r
