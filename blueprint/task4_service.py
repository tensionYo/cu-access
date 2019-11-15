# encoding = utf-8
from db.client import cli
from blueprint.task4_service import *

def device_interface_matching():
    sql = "select * from cu_trunk  where  equip_type1 ='LSW' and equip_type2 = 'LSW' or equip_type1 ='olt' and equip_type2 = 'olt';"
    equip_type_not_match = cli.fetchall(sql)
    sql1 = "select * from cu_trunk  where  port_type1 !='' and port_type_linked!= '' and port_type_linked != port_type1;"
    port_type_not_match = cli.fetchall(sql1)
    data = {}
    data['equip_type_not_match'] = equip_type_not_match
    data['port_type_not_match'] = port_type_not_match
    for i in equip_type_not_match:
        print(i)
    return data

def link_relation():
    sql = "select Link_name,is_trunk,Link_level,Link_physical_or_trunk_bandwidth,Network_element_name,Network_element_IP,slot_number,port_number," \
          "region,Subnet,Network_element_type,Network_element_role,Port_name,Port_type,Port_physical_bandwidth,Network_element_name1,Network_element_IP1," \
          "slot_number1,port_number1,region1,Subnet1,Network_element_type1,Network_element_role1,Port_name1,Port_type1,Port_physical_bandwidth1 from Link_name;"
    result = cli.fetchall(sql)
    for i in result:
        print(i)
    return result

def device_interface_matching_south():
    sql = "select cu.olt_id as 'olt_id',cu.slot_number1 as 'olt_slot_number', cu.pon_or_south_port_number as 'olt_port_number', cu.equip_id2 as 'OS_id', ft.ONUID as 'onu_id', ft.SPEED as 'speed', ft.USER_NAME as 'user_name', ft.LOGIN_NAME as 'login_name' " \
          " from cu_trunk cu LEFT JOIN FTTH_User_table ft " \
          " on ft.SY like CONCAT('%',cu.olt_id,'%') and ft.OLT_PORT like CONCAT('%',CONCAT(cu.slot_number1,'/',cu.pon_or_south_port_number),'%')"
    result = cli.fetchall(sql)
    return result

def update_FTTH_table():
    sql = "select * from FTTH_User_table ;"
    result = cli.fetchall(sql)
    # for i in result:
    #     OLT_IP = i['SY'].split("-")[0]
    #
    #print(result[1]['unicast_user_live'] == None)
    for i in 10:
        if result[i]['LOGIN_NAME'].find('@'):
            print(True)
        else:
            print(False)

