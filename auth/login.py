# encoding = utf-8
from flask_login import LoginManager
from db.client import cli


def get_user(login_name, password):
    """
    :type login_name: str
    :type password: str
    :param login_name:
    :param password:
    :return:
    """
    sql = "select user_id, login_name, password, is_admin from cu_user " \
          "where login_name = '{}' and password = '{}';".format(login_name, password)
    r = cli.fetchone(sql)
    return build_user_class(r)


def get_user_by_user_id(user_id):
    """
    :type user_id: str
    :param user_id:
    :return:
    """
    sql = "select user_id, login_name, password, is_admin from cu_user where user_id = '{}';".format(user_id)
    r = cli.fetchone(sql)
    return build_user_class(r)


def build_user_class(r):
    if not r:
        return None

    return User(r['user_id'], r['login_name'], r['password'], r['is_admin'])


login_manager = LoginManager()


class User:
    def __init__(self, user_id, login_name, password, is_admin):
        self.id = user_id
        self.login_name = login_name
        self.password = password
        self.is_admin = is_admin
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return unicode(self.id)


@login_manager.user_loader
def load_user(user_id):
    """
    :type user_id: unicode id
    :param user_id:
    :return:
    """
    user = get_user_by_user_id(str(user_id))
    return user
