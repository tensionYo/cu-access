# encoding = utf-8
import os


HOST = '0.0.0.0' if os.environ.get('ENV') == 'online' else 'localhost'
PORT = os.environ.get('PORT') or 5000
MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = os.environ.get('MYSQL_PORT', 3308)
# MYSQL_HOST = os.environ.get('MYSQL_HOST', '10.108.50.73')
# MYSQL_PORT = os.environ.get('MYSQL_PORT', 12580)

APP_SECRETE_KEY = 'q]@x8!5lf>O|!iWo_IYs@-C]@lYT.qtvN9smq`54gGR:K7.%[;o:+h|UzD3x.ZM!'



# MYSQL_CONFIG = {
#     'user': 'sjk',
#     'password': 'bni-jk',
#     'host': MYSQL_HOST,
#     'db': 'sjk_cu',
#     'port': MYSQL_PORT,
#     'autocommit': True
# }

MYSQL_CONFIG = {
    'user': 'root',
    'password': '123456zts',
    'host': MYSQL_HOST,
    'db': 'sjk_cu',
    'port': MYSQL_PORT,
    'autocommit': True
}

CORS_RESOURCES = {
    r'/*': {
        'origins': ['http://localhost:8080', 'http://172.20.10.11', 'http://10.128.239.215:8080','http://10.28.136.43:8080','http://127.0.0.1:5000',
                    'http://10.28.156.226:5000', 'http://192.168.43.207:8080', 'http://10.128.255.97:8080']
    }
}
