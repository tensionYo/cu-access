# coding=utf-8
from sklearn import linear_model

from db.client import query_list

clf = linear_model.LinearRegression()


# 多元线性回归函数LR
def LR(X, Y):
    clf.fit_intercept = False
    # if len(X) == len(Y):
    #     if len(X[0]) == len(Y):
    clf.fit(X, Y)
    return clf.coef_
    #     else:
    #         return 'error1'
    # else:
    #     return 'error2'


def parse_rate(s):
    return float(s.rstrip('Mb/s'))


def make_equation_factors(sql):
    res = query_list(sql)
    x = []
    y = []
    for r in res:
        c = r.keys()
        c.remove('v')
        c.sort()
        x.append([r[k] for k in c])
        y.append(parse_rate(r['v']))
    return x, y


def lr(x, y):
    res = LR(x, y)
    print res


if __name__ == '__main__':
    sql = 'SELECT 流入峰值 AS v, ' \
          '`_500m_count` AS a, ' \
          '`_300m_count` AS b, ' \
          '`_200m_count` AS c, ' \
          '`_100m_count` AS d ' \
          'FROM pon20180930 ' \
          'WHERE factor = 5 AND `_500m_count` > 0;'
    x, y = make_equation_factors(sql)
    lr(x, y)
