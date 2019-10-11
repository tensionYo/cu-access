# encoding = utf-8


def all_none(params):
    for i in params:
        if i:
            return False
    return True
