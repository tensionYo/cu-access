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

# def mapping_csv_to_jiawu():
#     sql = "select cu.id, cu.olt_id ,cu.port1, csv.ip , csv.port from " \
#           "cu_trunk as cu, pon_traffic_statistics_csv as csv " \
#           "where cu.id = csv.id and cu.equip_type1 = 'olt' and cu.north_port_type = '' ;"
#     result = cli.fetchall(sql)
#     for i in result:
#         print(i)
#         sql2 = "insert into mapping_csv_to_jiawu (csv_ip,csv_port,jiawu_olt_ip,jiawu_olt_port) values ('%s','%s','%s','%s')"%tuple([i['ip'],i['port'],i['olt_id'],i['port1']])
#         cli.execute(sql2)