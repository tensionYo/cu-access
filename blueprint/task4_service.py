# -*- coding: utf-8 -*-
from db.client import cli

"""change."""
def device_interface_matching():
    sql = "select * from cu_trunk  where  equip_type1 ='LSW' and equip_type2 = 'LSW' or equip_type1 ='olt' and equip_type2 = 'olt';"
    equip_type_not_match = cli.fetchall(sql)
    sql1 = "select * from cu_trunk  where  north_port_type !='' and port_type_linked!= '' and port_type_linked != north_port_type;"
    port_type_not_match = cli.fetchall(sql1)
    data = {}
    data['equip_type_not_match'] = equip_type_not_match
    data['port_type_not_match'] = port_type_not_match
    for i in equip_type_not_match:
        print(i)
    return data
"""not change."""
def link_relation():
    sql = "select Link_name,is_trunk,Link_level,Link_physical_or_trunk_bandwidth,Network_element_name,Network_element_IP,port_number," \
          "region,Subnet,Network_element_type,Network_element_role,Port_name,Port_type,Port_physical_bandwidth,Network_element_name1,Network_element_IP1," \
          "port_number1,region1,Subnet1,Network_element_type1,Network_element_role1,Port_name1,Port_type1,Port_physical_bandwidth1 from link_name;"
    result = cli.fetchall(sql)
    for i in result:
        print(i)
    return result
"""change. """
def device_interface_matching_south():
    sql = "select cu.olt_id as 'olt_id',cu.port1 as 'olt_port', cu.equip_id_link as 'OS_id', od.onu_ip as 'onu_ip', od.ONUID as 'onu_id',od.type as 'onu_type', od.onu_manufacture as 'onu_manufacture', od.serial_number as 'onu_serial_number'" \
          " from cu_trunk cu LEFT JOIN cu_onu_device od " \
          " on od.OLT_IP = cu.olt_id and od.OLT_PORT = cu.port1 ;"
    result = cli.fetchall(sql)
    print(result)
    return result

# def update_FTTH_table():
#     sql = "select * from ftth_user_table ;"
#     result = cli.fetchall(sql)
#
#     for i in result:
#         id = i['id']
#         OLT_IP = i['SY'].split('-')[0]
#         print(i)
#         if i['LOGIN_NAME']== None:
#             boardband_VLAN = i['SERIAL_NUMBER']
#             sql = " update ftth_user_table set boardband_VLAN = '%s', OLT_IP = '%s' where id = '%s';"%tuple([boardband_VLAN,OLT_IP,id])
#             cli.execute(sql)
#             print("None")
#         elif '@' in i['LOGIN_NAME']:
#             is_multicast_user = 'n'
#             multicast_user_live = "1000"
#             multicast_user_demand = i['LOGIN_NAME']
#             unicast_user_live = i['LOGIN_NAME'].split('@')[0]
#             unicast_user_demand = '0'+unicast_user_live
#             boardband_VLAN = i['SERIAL_NUMBER']
#             sql = " update ftth_user_table set is_multicast_user = '%s', multicast_user_live = '%s',multicast_user_demand = '%s',unicast_user_live = '%s',unicast_user_demand = '%s',boardband_VLAN = '%s',OLT_IP = '%s' where id = '%s';" % tuple([is_multicast_user,multicast_user_live,multicast_user_demand,unicast_user_live,unicast_user_demand,boardband_VLAN, OLT_IP, id])
#             cli.execute(sql)
#             print("IPTV")
#         else:
#             is_multicast_user = 'y'
#             multicast_user_live = "1000"
#             multicast_user_demand = i['LOGIN_NAME']
#             boardband_VLAN = i['SERIAL_NUMBER']
#             sql = " update ftth_user_table set is_multicast_user = '%s', multicast_user_live = '%s',multicast_user_demand = '%s',boardband_VLAN = '%s',OLT_IP = '%s' where id = '%s';" % tuple([is_multicast_user, multicast_user_live, multicast_user_demand, boardband_VLAN, OLT_IP, id])
#             cli.execute(sql)
#             print("bandwidth.")


def Link_tree():
    sql1 = " select la.Broadband_account as Broadband_account,la.bandwidth as bandwidth,la.IPTV_account as IPTV_account," \
           "la.MDUIP as MDUIP, la.MDU_port as MDU_port, cu.equip_id_link as OS_id, cu.olt_id as olt_id, cu.port1 as olt_down_port " \
           "from lan_user_table la LEFT JOIN cu_trunk cu on la.OLT_IP = cu.olt_id and la.PON = cu.port1 " \
           "where la.id<20 ;"
    result = cli.fetchall(sql1)

    """olt_down_port to up_port."""
    sql2 = "select * from cu_trunk where if_olt_up_or_down = 'y' ;"
    result2 = cli.fetchall(sql2)
    olt_ip = []
    port_count = []
    port=[]
    for i in result2:
        if (i['olt_id'] not in olt_ip):
            olt_ip.append(i['olt_id'])
            port_count.append(1)
            port.append([])
            port[olt_ip.index(i['olt_id'])].append(i['port1'])
        else:
            port_count[olt_ip.index(i['olt_id'])]+=1
            port[olt_ip.index(i['olt_id'])].append(i['port1'])
    count = [0]*len(olt_ip)
    # print(count)
    # print(olt_ip)
    # print(port_count)
    # print(port)

    """LSW_down_port to up_port"""
    LSW_ip = []
    LSW_port_count = []
    LSW_port = []
    sql4 = "select * from cu_trunk where north_port_type != '' and equip_type1 = 'LSW' and equip_id_link = '';"
    result4 = cli.fetchall(sql4)
    for i in result4:
        if (i['olt_id'] not in LSW_ip):
            LSW_ip.append(i['olt_id'])
            LSW_port_count.append(1)
            LSW_port.append([])
            LSW_port[LSW_ip.index(i['olt_id'])].append(i['port1'])
        else:
            LSW_port_count[LSW_ip.index(i['olt_id'])] += 1
            LSW_port[LSW_ip.index(i['olt_id'])].append(i['port1'])
    LSW_count = [0] * len(LSW_ip)

    print(LSW_ip)
    print(LSW_port_count)
    print(LSW_port)
    print(LSW_count)

    for i in result:
        """olt_south_port to north_port"""
        index = olt_ip.index(i['olt_id'])
        count[index]+=1
        choosed_olt_up_port_index = count[index]%port_count[index]
        i['choosed_olt_up_port'] = port[index][choosed_olt_up_port_index]
        #print(i)

        """olt_up_port to LSW_down_port"""
        sql3 = "select Network_element_IP1,port_number1 from link_name where link_level = 'OLT-LSW' and Network_element_IP = '%s' and port_number = '%s';"%tuple([i['olt_id'],i['choosed_olt_up_port']])
        result3 = cli.fetchone(sql3)
        i['LSW_IP'] = result3['Network_element_IP1']
        i['LSW_down_port'] = result3['port_number1']

        """LSW_down_port to up_port"""
        index_lsw = LSW_ip.index(i['LSW_IP'])
        LSW_count[index_lsw]+=1
        choosed_lsw_up_port_index = LSW_count[index_lsw] % LSW_port_count[index_lsw]
        i['choosed_lsw_up_port'] = LSW_port[index_lsw][choosed_lsw_up_port_index]


        """LSW_up_port to BRAS """
        sql5 = "select Network_element_IP,port_number from link_name where link_level = 'BRAS-LSW' and Network_element_IP1 = '%s' and port_number1 = '%s';"%tuple([i['LSW_IP'],i['choosed_lsw_up_port']])
        result5 = cli.fetchone(sql5)
        i['BRAS_IP'] = result5['Network_element_IP']
        i['BRAS_port'] = result5['port_number']



        """BRAS_port to up"""
        sql6 = "select * from link_name where link_level = 'BRAS-SR' or link_level = 'BRAS-CR'or link_level = 'BRAS-CDN'and Network_element_IP = '%s' and port_number = '%s';"%tuple([i['BRAS_IP'],i['BRAS_port']])
        result6 = cli.fetchall(sql6)
        for j in result6:
            i[j['Network_element_type1']+'_IP'] = j['Network_element_IP1']
            i[j['Network_element_type1'] + '_port'] = j['port_number1']
        print(i)

    return result

def PON_device_power():
    sql = "select * from cu_olt_device ;"
    result = cli.fetchall(sql)
    table_data = []
    count = 0
    view_pon_user_number = [0,0,0,0]
    view_olt_up_road = [0,0,0,0,0]
    view_slot_occupy_rate = [0,0,0,0]
    view_pon_used_rate = [0,0,0,0]
    for i in result:
        """data1"""
        count += 1
        table_data.append({})
        table_data[count - 1]['id'] = i['id']
        table_data[count - 1]['OLT_IP'] = i['OLT_IP']
        # return_result[count - 1]['up_limmit'] = i['OLT_IP']
        table_data[count - 1]['slot_occupy_rate'] = 1.0*int(i['used_service_slot_count']) / int(i['service_slot_count'])
        table_data[count - 1]['up_port_occupy_rate'] = 1.0*int(i['upport_upstream_flow_sum']) / int(i['PON_port_upstream_band_nominal_capacity'])
        table_data[count - 1]['PON_port_occupy_rate'] = 1.0*int(i['pon_port_used_count']) / int(i['pon_port_config_count'])
        sql = "select count(*) as count from lan_user_table where OLT_IP = '%s' ;" % i['OLT_IP']
        table_data[count - 1]['user_number'] = cli.fetchall(sql)[0]['count']

        """data2"""
        if table_data[count - 1]['user_number']>0 and table_data[count - 1]['user_number']<500:
            view_pon_user_number[0]+=1
        elif table_data[count - 1]['user_number']>=500 and table_data[count - 1]['user_number'] <1000:
            view_pon_user_number[1] += 1
        elif table_data[count - 1]['user_number']>=1000 and table_data[count - 1]['user_number'] <1500:
            view_pon_user_number[2] += 1
        else:
            view_pon_user_number[3] += 1
        up = i['north_10GE_port_count']*10+i['north_GE_port_count']
        if up==1:
            view_olt_up_road[0]+=1
        elif up == 2:
            view_olt_up_road[1] += 1
        elif up == 3:
            view_olt_up_road[2] += 1
        elif up == 4:
            view_olt_up_road[3] += 1
        else:
            view_olt_up_road[4] += 1

        if table_data[count - 1]['slot_occupy_rate'] >0.0 and table_data[count - 1]['slot_occupy_rate'] < 0.3:
            view_slot_occupy_rate[0]+=1
        elif table_data[count - 1]['slot_occupy_rate'] >0.3 and table_data[count - 1]['slot_occupy_rate'] < 0.5:
            view_slot_occupy_rate[1] += 1
        elif table_data[count - 1]['slot_occupy_rate'] >0.5 and table_data[count - 1]['slot_occupy_rate'] < 0.7:
            view_slot_occupy_rate[2] += 1
        else:
            view_slot_occupy_rate[3] += 1

        if table_data[count - 1]['PON_port_occupy_rate'] >0.0 and table_data[count - 1]['PON_port_occupy_rate'] < 0.3:
            view_pon_used_rate[0]+=1
        elif table_data[count - 1]['PON_port_occupy_rate'] >0.3 and table_data[count - 1]['PON_port_occupy_rate'] < 0.5:
            view_pon_used_rate[1] += 1
        elif table_data[count - 1]['PON_port_occupy_rate'] >0.5 and table_data[count - 1]['PON_port_occupy_rate'] < 0.7:
            view_pon_used_rate[2] += 1
        else:
            view_pon_used_rate[3] += 1

    view_data = {}
    view_data['view_pon_user_number'] = {}
    view_data['view_pon_user_number']['0-500'] = view_pon_user_number[0]
    view_data['view_pon_user_number']['500-1000'] = view_pon_user_number[1]
    view_data['view_pon_user_number']['1000-1500'] = view_pon_user_number[2]
    view_data['view_pon_user_number']['>2000'] = view_pon_user_number[3]
    view_data['view_olt_up_road'] = {}
    view_data['view_olt_up_road']['1*GE'] = view_olt_up_road[0]
    view_data['view_olt_up_road']['2*GE'] = view_olt_up_road[1]
    view_data['view_olt_up_road']['3*GE'] = view_olt_up_road[2]
    view_data['view_olt_up_road']['4*GE'] = view_olt_up_road[3]
    view_data['view_olt_up_road']['5*GE'] = view_olt_up_road[4]
    view_data['view_slot_occupy_rate'] = {}
    view_data['view_slot_occupy_rate']['0-30%'] =view_slot_occupy_rate[0]
    view_data['view_slot_occupy_rate']['30%-50%'] = view_slot_occupy_rate[1]
    view_data['view_slot_occupy_rate']['50%-70%'] = view_slot_occupy_rate[2]
    view_data['view_slot_occupy_rate']['70%-100%'] = view_slot_occupy_rate[3]
    view_data['view_pon_used_rate'] = {}
    view_data['view_pon_used_rate']['0-30%'] = view_pon_used_rate[0]
    view_data['view_pon_used_rate']['30%-50%'] = view_pon_used_rate[1]
    view_data['view_pon_used_rate']['50%-70%'] = view_pon_used_rate[2]
    view_data['view_pon_used_rate']['70%-100%'] = view_pon_used_rate[3]
    data = {}
    data['table_data'] = table_data
    data['view_data'] = view_data

    return data



