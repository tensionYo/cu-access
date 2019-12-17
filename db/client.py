# encoding=utf-8
from mysql.connector.cursor import MySQLCursorBufferedDict
from mysql.connector.pooling import MySQLConnectionPool

from conf.config import MYSQL_CONFIG

__pool = None


def get_mysql_connection_pool():
    global __pool
    if __pool:
        return __pool
    __pool = MySQLConnectionPool(**MYSQL_CONFIG)
    return __pool




class MySQLClient:
    def __init__(self):
        self.cp = get_mysql_connection_pool()

    def fetchall(self, sql):
        con = self.cp.get_connection()
        cur = con.cursor(cursor_class=MySQLCursorBufferedDict)
        cur.execute(sql)
        r = cur.fetchall()
        cur.close()
        con.close()
        return r

    def fetchone(self, sql):
        con = self.cp.get_connection()
        cur = con.cursor(cursor_class=MySQLCursorBufferedDict)
        cur.execute(sql)
        r = cur.fetchone()
        cur.close()
        con.close()
        return r

    def execute(self, sql):
        con = self.cp.get_connection()
        cur = con.cursor(cursor_class=MySQLCursorBufferedDict)
        # cur.execute('start transaction;')
        cur.execute(sql)
        # cur.execute('commit;')
        cur.close()
        con.close()


cli = MySQLClient()

if __name__ == '__main__':
    config = {
        'user': 'dev_user',
        'password': '5ecr3t',
        'host': 'localhost',
        'db': 'cu',
        'port': 3306
    }
    res = cli.fetchall('SELECT * FROM cu_olt')
    print res
    res = cli.fetchone('SELECT id, city_name FROM pon_traffic_statistics_csv LIMIT 1')
    print res
