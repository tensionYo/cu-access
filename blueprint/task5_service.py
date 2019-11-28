# encoding = utf-8
from db.client import cli

def show_meal_thresholdset_table():
    sql = "select * from threshold_meal ;"
    result = cli.fetchall(sql)
    print(result)
    return result

def show_device_thresholdset_table():
    sql = "select * from threshold_device ;"
    result = cli.fetchall(sql)
    print(result)
    return result

def show_port_thresholdset_table():
    sql = "select * from threshold_port ;"
    result = cli.fetchall(sql)
    print(result)
    return result

def update_meal_threshold_table(params):
    sql = "update threshold_meal SET meal_type = '%s',down_direction__down_limit = '%s',down_direction__up_limit = '%s',up_direction_down_limit = '%s',up_direction_up_limit = '%s' where id = '%s'"%tuple(params)
    cli.execute(sql)


def update_device_threshold_table(params):
    sql = "update threshold_device SET device_type = '%s',port_type = '%s',port_num = '%s',user_num_up_boundary = '%s',split_user_up_limit = '%s' where id = '%s'" % tuple(params)
    cli.execute(sql)

def update_port_threshold_table(params):
    sql = "update threshold_port SET device_type = '%s',port_type = '%s',port_level = '%s',down_direction_warn_up_limit = '%s',up_direction_warn_up_limit = '%s'," \
          "down_direction_start_up_limit = '%s',up_direction_start_up_limit = '%s',user_num_up_boundray = '%s',FTTB_split_user_num_up_boundary = '%s' where id = '%s'" % tuple(params)
    cli.execute(sql)