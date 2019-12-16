# -*- coding: utf-8 -*-
from db.client import cli


"""
def AllFromTableIPTV_concurrence_user_num():
    sql = "select * from IPTV_concurrence_user_num ;"
    result = cli.fetchall(sql)
    return result

def AllFromTableBRAS_online_user_num():
    sql = "select * from BRAS_online_user_num ;"
    result = cli.fetchall(sql)
    return result

"""

def DateAndNumFromTableIPTV_concurrence_user_num(time):
    temp = '%'+time+'%'
    sql = "select start_time,user_num from iptv_concurrence_user_num where start_time like '%s';" %temp
    result = cli.fetchall(sql)
    print(result)
    for i in result:
        time = i['start_time'].split(" ")
        i.update({'start_time': time[0]})
    print(result)
    return result


def DateAndNumFromTableBRAS_online_user_num(time):
    temp = '%' + time + '%'
    sql = "select start_time,user_num from bras_online_user_num where start_time like '%s';" %temp
    result = cli.fetchall(sql)
    for i in result:
        time = i['start_time'].split(" ")
        i.update({'start_time': time[0]})
    print(result)
    return result

def AllFromTableBRASUserNum(time):
    temp = '%' + time + '%'
    sql = "select start_time,level_first,level_second,level_third,level_forth,level_fifth from bras_online_user_num where start_time like '%s';" % temp
    result = cli.fetchall(sql)
    returnTime = []
    return100 = []
    return200 = []
    return300 = []
    return500 = []
    return600 = []
    total = []
    for i in result:
        time = i['start_time'].split(" ")
        returnTime.append(time[0])
        return100.append(i['level_first'])
        return200.append(i['level_second'])
        return300.append(i['level_third'])
        return500.append(i['level_forth'])
        return600.append(i['level_fifth'])
        total.append(i['level_first']+i['level_second']+i['level_third']+i['level_forth']+i['level_fifth'])
    dic={}
    dic['returnTime'] = returnTime
    dic['return100'] = return100
    dic['return200'] = return200
    dic['return300'] = return300
    dic['return500'] = return500
    dic['return600'] = return600
    dic['total'] = total
    print(dic)
    return dic



# not test
def  packagingRegisterUserReturnType(resultIPTV,resultBRAS):
    returnTime,returnIPTV,returnBRAS = [],[],[]
    for i in range(len(resultIPTV)):
        returnTime.append(resultIPTV[i]['start_time'])
        returnIPTV.append(resultIPTV[i]['user_num'])
        returnBRAS.append(resultBRAS[i]['user_num'])

    dic = {}
    dic['returnTime'] = returnTime
    dic['returnIPTV'] = returnIPTV
    dic['returnBRAS'] = returnBRAS
    return dic




def initBRAS_online_user_num():
    sql1 = "select * from bras_online_user_num ;"
    result1 = cli.fetchall(sql1)
    k = 1
    for i in result1:
        total = i['level_first']+i['level_second']+i['level_third']+i['level_forth']+i['level_fifth']
        vs = tuple([total,total/5,k])
        sql2 = "update bras_online_user_num SET user_num = '%s',online_service_total = '%s' where id = '%s' ;" %vs
        print()
        cli.execute(sql2)
        k+=1




def initIPTV_concurrence_user_num():
    sql1 = "select * from iptv_concurrence_user_num ;"
    result1 = cli.fetchall(sql1)
    k = 1
    for i in result1:
        baseNum = i['level_first_VOD']+i['level_second_VOD']+i['level_first_LIVE']+i['level_first_TSTV']+i['level_first_TVOD']
        unicast_simultaneously = i['level_first_VOD']+i['level_second_VOD']+i['level_first_TSTV']+i['level_first_TVOD']
        user_num = baseNum * 3
        multicast_simultaneously = baseNum * 2
        CDN_total_num = baseNum
        CDN_total = (i['level_first_LIVE']+multicast_simultaneously)*i['LIVE_aver_bandwidth']+(i['level_first_VOD']+i['level_second_VOD'])*i['VOD_aver_bandwidth']+i['level_first_TSTV']*i['TSTV_aver_bandwidth']+i['level_first_TVOD']*i['TVOD_aver_bandwidth']
        vs = tuple([user_num,unicast_simultaneously,multicast_simultaneously,CDN_total_num,CDN_total,k])
        sql2 = "update iptv_concurrence_user_num SET user_num = '%s',unicast_simultaneously = '%s', multicast_simultaneously = '%s', CDN_total_num = '%s', CDN_total = '%s' where id = '%s' ;" %vs
        print()
        cli.execute(sql2)
        k += 1

def calculateParametersWithIPTVAndBRAS(time):
    temp = '%' + time + '%'
    sql = "select count(*) as count from iptv_concurrence_user_num where start_time like '%s';" %temp
    sql1 = "select * from iptv_concurrence_user_num where start_time like '%s';" %temp
    sql2 = "select * from bras_online_user_num where start_time like '%s';" %temp
    sql3 = "select total_channel_bandwidth_request as SD_rate from live_channel_bandwidth where type like '%s';" %'%sd%'
    sql4 = "select sum(total_channel_bandwidth_request)  as HD_rate from live_channel_bandwidth where type like '%s';" %'%hd%'
    sql5 = "select sum(total_channel_bandwidth_request) as K_rate from live_channel_bandwidth where type like '%s';" %'%K%'
    count = cli.fetchall(sql)
    print(count)
    result1 = cli.fetchall(sql1)
    result2 = cli.fetchall(sql2)
    SD_rate = cli.fetchall(sql3)
    HD_rate = cli.fetchall(sql4)
    K_rate = cli.fetchall(sql5)
    time = []
    infiltration_ratio = []
    demand_rate_ave = []
    demand_simultaneously = []
    broadband_user_demand_rate_ave = []
    live_user_rate_ave = []
    live_simultaneously = []
    broadband_user_live_rate_ave = []
    online_user_simultaneously = []
    online_user_rate_ave = []
    broadband_user_online_rate_ave = []
    broadband_user_rate_ave = []
    for i in range(count[0]['count']):
        temp = result1[i]['start_time'].split(" ")
        time.append(temp[0])
        infiltration_ratio.append(result1[i]['user_num']*2.0/result2[i]['user_num']/1.4)
        demand_rate_ave.append(result1[i]['CDN_total']*1.0/result1[i]['CDN_total_num'])
        demand_simultaneously.append(result1[i]['unicast_simultaneously']/2.0/result1[i]['user_num'])
        broadband_user_demand_rate_ave.append(infiltration_ratio[i]*demand_rate_ave[i]*demand_simultaneously[i])
        live_user_rate_ave.append(2/143*K_rate[0]['K_rate']+29/143.0*HD_rate[0]['HD_rate']+112/143.0*SD_rate[0]['SD_rate'])
        live_simultaneously.append((result1[i]['level_first_LIVE']+result1[i]['multicast_simultaneously'])/2.0/result1[i]['user_num'])
        broadband_user_live_rate_ave.append(live_user_rate_ave[i]*live_simultaneously[i]*infiltration_ratio[i])
        online_user_simultaneously.append(0.7)
        online_user_rate_ave.append(2)
        broadband_user_online_rate_ave.append(online_user_rate_ave[i]*online_user_simultaneously[i])
        broadband_user_rate_ave.append((broadband_user_live_rate_ave[i]+live_simultaneously[i])*1.1+infiltration_ratio[i])

    dic = {}
    dic['time'] = time
    dic['infiltration_ratio'] = infiltration_ratio
    dic['demand_rate_ave'] = demand_rate_ave
    dic['demand_simultaneously'] = demand_simultaneously
    dic['broadband_user_demand_rate_ave'] = broadband_user_demand_rate_ave
    dic['live_user_rate_ave'] = live_user_rate_ave
    dic['live_simultaneously'] = live_simultaneously
    dic['broadband_user_live_rate_ave'] = broadband_user_live_rate_ave
    dic['online_user_simultaneously'] = online_user_simultaneously
    dic['online_user_rate_ave'] = online_user_rate_ave
    dic['broadband_user_online_rate_ave'] = broadband_user_online_rate_ave
    dic['broadband_user_rate_ave'] = broadband_user_rate_ave
    print(dic)
    return dic

def AllfromTableStation():
    sql = "select * from station ;"
    result = cli.fetchall(sql)
    print(result)
    return result

def AllDevicesByStationId(id):
    sql_brascrsr = " select * from cu_brascrsr_device where station = '%s' ;" %id
    sql_olt = " select * from cu_olt_device where Stations_of_OLT = '%s' ;" %id
    result1 = cli.fetchall(sql_brascrsr)
    result2 = cli.fetchall(sql_olt)
    olt=[]
    brascrsr=[]
    for i in result1:
        tempdic1 ={}
        tempdic1['id'] = i['id']
        tempdic1['ip'] = i['IP']
        tempdic1['type'] = i['type']
        tempdic1['name'] = i['Name']
        brascrsr.append(tempdic1)
    for i in result2:
        tempdic2 = {}
        tempdic2['id'] = i['id']
        tempdic2['ip'] = i['OLT_IP']
        tempdic2['type'] = "OLT"
        tempdic2['name'] = i['OLT_Name']
        olt.append(tempdic2)
    result = []
    tempdic = {}
    tempdic['brascrsr'] = brascrsr
    tempdic['olt'] = olt
    result.append(tempdic)
    print(result)
    return result

def ShowInfomationOfDeviceByIdAndType(id):

    sql = "select OLT_IP as ip from cu_olt_device where id = '%s'; "%id
    ip = cli.fetchone(sql)['ip']
    print(ip)
    sql = "select * from cu_olt_slot where olt_ip = '%s';" %ip
    result = cli.fetchall(sql)
    print(result)
    return result









