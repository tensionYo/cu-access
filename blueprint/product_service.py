# encoding = utf-8
from db.client import cli


def add_product(params):
    """
    :type params: list
    :param params:
    :return:
    """
    # TODO fix sql and table
    vs = tuple(params)
    sql = "insert into xxx (bandwidth, delay, packet_loss_rate) " \
          "VALUES '%s', '%s', '%s';" % vs
    cli.execute(sql)
