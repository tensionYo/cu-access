# encoding = utf-8


def all_none(params):
    for i in params:
        if i:
            return False
    return True


def parse_traffic_rate(s):
    """
    :type s: str
    :param s:
    :return:
    """
    if not s:
        return 0
    if s.endswith('Mb/s'):
        return int(float(s[:len(s) - 4]))
    else:
        return -1


def check_eval_matrix(m):
    """
    :type m: list[list[flost]]
    :param m:
    :return:
    """
    try:
        fm = [map(float, r) for r in m]
        rn, cn = len(m), len(m[0])
        if rn != cn:
            return None, False
        for r in range(rn, rn):
            for c in range(cn):
                if abs(fm[r][c] * fm[c][r] - 1) > 0.0001:
                    return None, False
        return fm, True
    except Exception as e:
        return None, False
