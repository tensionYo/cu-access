# encoding = utf-8
from db.client import cli
from blueprint.task3_service import *
from blueprint.task5_service import *


def AllFromTableBusiness_parameters():
    sql = "select * from business_parameters;"
    result = cli.fetchall(sql)
    return result

def ALLFromTable4K():
    sql = "select * from network_requirements_for_4K ;"
    result = cli.fetchall(sql)
    return result

def AllFromTableSet_Meal():
    sql = " select * from set_meal ;"
    result = cli.fetchall(sql)
    return result

def AllFromTableLive_channel_bandwidth():
    sql = "select * from live_channel_bandwidth ;"
    result = cli.fetchall(sql)
    return result

def InsertIntoTableBusiness_parameters(params):
    vs = tuple(params)
    sql = "insert into business_parameters (type, Resolving_power, Frame_rate,Color_bits,compression_technique,Minimum_rate) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % vs
    cli.execute(sql)

def InsertIntoTable4K(params):
    vs = tuple(params)
    sql = "insert into network_requirements_for_4K (type, bandwidth, time_delay,Packet_loss_rate) VALUES ('%s', '%s', '%s', '%s');" % vs
    cli.execute(sql)

def InsertIntoTableSet_Meal(params):
    vs = tuple(params)
    sql = "insert into set_meal (Set_meal_type,Broadband_commitment_uplink,Broadband_commitment_downlink,IPTV_commitment_uplink," \
          "IPTV_commitment_downlink,OLT_uplink_minimum_bandwidth,OLT_uplink_maximum_bandwidth,OLT_downlink_minimum_bandwidth,OLT_downlink_maximum_bandwidth," \
          "BRAS_uplink_minimum_bandwidth,BRAS_uplink_maximum_bandwidth,BRAS_downlink_minimum_bandwidth,BRAS_downlink_maximum_bandwidth," \
          "Broadband_VLAN,On_demand_VLAN,Live_broadcast_VLAN) VALUES ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s');"% vs
    cli.execute(sql)

def InsertIntoTableLive_channel_bandwidth(params):
    vs = tuple(params)
    sql = " insert into live_channel_bandwidth (type,channel_num,one_channel_bandwidth_request,total_channel_bandwidth_request)" \
          "VALUES ('%s', '%s', '%s', '%s')" % vs
    cli.execute(sql)

def DeleteFromTableBusiness_parameters(id):
    sql = "delete from business_parameters where id = '%s';" %id
    cli.execute(sql)

def DeleteFromTable4K(id):
    sql = "delete from network_requirements_for_4K where id = '%s';" %id
    cli.execute(sql)

def DeleteFromTableSet_Meal(id):
    sql = "delete from set_meal where id = '%s';" % id
    cli.execute(sql)

def DeleteFromTableLive_channel_bandwidth(id):
    sql = "delete from live_channel_bandwidth where id = '%s'"% id
    cli.execute(sql)

def UpdateFromTableBusiness_parameters(params):
    vs = tuple(params)
    sql = "update business_parameters SET type = '%s',Resolving_power = '%s', Frame_rate =  '%s'," \
          "Color_bits =  '%s',compression_technique =  '%s',Minimum_rate =  '%s' where id =  '%s';"% vs
    cli.execute(sql)

def UpdateFromTable4K(params):
    vs = tuple(params)
    sql = "update network_requirements_for_4K SET type = '%s',bandwidth = '%s', time_delay =  '%s'," \
          "Packet_loss_rate =  '%s' where id = '%s' ;"% vs
    cli.execute(sql)

def UpdateFromTableSet_Meal(params):
    vs = tuple(params)
    sql = "update set_meal SET Set_meal_type = '%s',Broadband_commitment_uplink = '%s', Broadband_commitment_downlink =  '%s',IPTV_commitment_uplink =  '%s',IPTV_commitment_downlink =  '%s'," \
          "OLT_uplink_minimum_bandwidth =  '%s',OLT_uplink_maximum_bandwidth =  '%s',OLT_downlink_minimum_bandwidth =  '%s',OLT_downlink_maximum_bandwidth =  '%s', " \
          "BRAS_uplink_minimum_bandwidth =  '%s',BRAS_uplink_maximum_bandwidth =  '%s',BRAS_downlink_minimum_bandwidth =  '%s',BRAS_downlink_maximum_bandwidth =  '%s'," \
          "Broadband_VLAN =  '%s',On_demand_VLAN =  '%s',Live_broadcast_VLAN =  '%s'  where id =  '%s';" % vs
    cli.execute(sql)

def UpdateFromTableLive_channel_bandwidth(params):
    vs = tuple(params)
    sql = "update live_channel_bandwidth SET type='%s', channel_num='%s', one_channel_bandwidth_request='%s', total_channel_bandwidth_request='%s' where id = '%s';" % vs
    cli.execute(sql)



if __name__ == '__main__':
    """InsertIntoTableBusiness_parameters(['hhh','2','2','2','2','2'])
        UpdateFromTableBusiness_parameters(['hhh','22','22','22','22','22',21])
        DeleteFromTableBusiness_parameters(20)
        InsertIntoTable4K(['name1','>112','<221','<22'])
        UpdateFromTable4K(['name21','>2','<1','<2',5])
        DeleteFromTable4K(6)
        InsertIntoTableSet_Meal(['hhh','21','21','21','21','2','2','2','2','2','2','2','2','2','2','2'])
        UpdateFromTableSet_Meal(['h','1','1','1','1','2','2','2','2','2','2','2','2','2','2','2',11])
        DeleteFromTableSet_Meal(12)
        InsertIntoTableLive_channel_bandwidth(['1','1','1','1'])
        UpdateFromTableLive_channel_bandwidth(['11','11','11','11','10'])
        DeleteFromTableLive_channel_bandwidth(10)
        initBRAS_online_user_num()
        initIPTV_concurrence_user_num()
        DateAndNumFromTableIPTV_concurrence_user_num("2017/7")
        DateAndNumFromTableBRAS_online_user_num("2017/7")
        calculateParametersWithIPTVAndBRAS("2019/10")
        ShowInfomationOfDeviceByIdAndType(7)
        DateAndNumFromTableBRAS_online_user_num("2017/6")
        calculateParametersWithIPTVAndBRAS("2017/6")
        
        device_interface_matching()
        link_relation()
    """
    update_port_threshold_table(['OLT','up_port',"GE",0.501,0.5,0.65,0.65,0,0,1])









