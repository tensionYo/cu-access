# encoding = utf-8
import json
import functools

from flask_login import current_user


def admin_role(func):
    @functools.wraps(func)
    def __func(*args, **kwargs):
        if not current_user.is_admin:
            return dict(success=False, msg='You are not Admin User.')
        return func(*args, **kwargs)

    return __func


def json_resp(func):
    @functools.wraps(func)
    def __func(*args, **kwargs):
        resp = func(*args, **kwargs)
        if isinstance(resp, dict):
            if 'success' not in resp:
                resp = dict(success=True, data=resp)
        elif isinstance(resp, (int, float, str, list)):
            return dict(success=True, data=resp)
        else:
            raise TypeError('response should be instance of dict.')
        return json.dumps(resp)

    return __func


if __name__ == '__main__':
    @json_resp
    def f(s):
        return s


    r = f('hello')
    assert 'success' in r
    print r
