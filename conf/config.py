# encoding = utf-8
import os


HOST = '0.0.0.0' if os.environ.get('ENV') == 'online' else 'localhost'
PORT = os.environ.get('PORT') or 8080
MYSQL_HOST = os.environ.get('MYSQL_HOST', '10.108.50.171')
MYSQL_PORT = os.environ.get('MYSQL_PORT', 12580)


MYSQL_CONFIG = {
    'user': 'dev_user',
    'password': '5ecr3t',
    'host': MYSQL_HOST,
    'db': 'cu',
    'port': MYSQL_PORT
}

CORS_RESOURCES = {
    r'/*': {
        'origins': ['http://localhost:8088', 'http://192.168.23.3:8080', 'http://10.128.239.215:8080',
                    'http://10.128.249.26:8080', 'http://192.168.43.207:8080', 'http://10.128.255.97:8080']
    }
}
