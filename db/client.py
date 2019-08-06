# encoding=utf-8
from threading import RLock
from multiprocessing import Pool
from mysql.connector import MySQLConnection, Error
from mysql.connector.pooling import MySQLConnectionPool
from conf.config import MYSQL_CONFIG

__pool = None


def __init():
    global __pool
    if not __pool:
        __pool = MySQLConnectionPool(10, **MYSQL_CONFIG)


__init()


def __wrap(columns, row):
    e = {k: v for k, v in zip(columns, row)}
    return e


def query_list(sql):
    con = __pool.get_connection()
    c = con.cursor()
    c.execute(sql)
    rows = c.fetchall()
    columns = c.column_names
    c.close()
    con.close()
    if not rows:
        return []
    return [__wrap(columns, i) for i in rows]


def query_one(sql):
    con = __pool.get_connection()
    c = con.cursor(buffered=True)
    c.execute(sql)
    row = c.fetchone()
    columns = c.column_names
    c.close()
    con.close()
    if not row:
        return {}
    return __wrap(columns, row)


class MySQLClient(object):
    _lock = RLock()
    __instance = None

    @staticmethod
    def query_list(sql):
        global __pool
        con = __pool.get_connection()
        c = con.cursor()
        c.execute(sql)
        return []

    @staticmethod
    def get_instance(**kwargs):
        with MySQLClient._lock:
            if not MySQLClient.__instance:
                ins = MySQLClient(**kwargs)
                MySQLClient.__instance = ins

        return MySQLClient.__instance

    def __init__(self, **config):
        with MySQLClient._lock:
            if MySQLClient.__instance:
                raise Exception('!!! singleton class !!!')
            else:
                self.__instance = MySQLClient(**config)
                self.__instance.autocommit = True
                self.cursor = self.__instance.cursor()

    def query(self, sql):
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return self.__wrap(rows)

    def query_one(self, sql):
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        res = {k: v for k, v in zip(self.cursor.column_names, row)}
        return res

    def __wrap(self, rows):
        res = []
        columns = self.cursor.column_names
        for row in rows:
            e = {k: v for k, v in zip(columns, row)}
            res.append(e)
        return res

    def execute(self, sql):
        self.cursor.execute(sql)


__cli = None


def get_mysql_client():
    global __cli
    if __cli:
        return __cli
    else:
        __cli = MySQLClient.get_instance(**MYSQL_CONFIG)
        return __cli


if __name__ == '__main__':
    config = {
        'user': 'dev_user',
        'password': '5ecr3t',
        'host': 'localhost',
        'db': 'cu',
        'port': 3306
    }
    cli = MySQLClient.get_instance(**config)
    res = cli.query('SELECT * FROM cu_olt')
    print res
    res = cli.query_one('SELECT id, city_name FROM pon_traffic_statistics_csv LIMIT 1')
    print res
