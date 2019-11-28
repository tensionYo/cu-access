# encoding = utf-8
from flask import Blueprint, request
from flask_login import login_required
from utils.decorator import json_resp, admin_role
from task3_service import *


bp = Blueprint('task1_bp2', __name__, url_prefix='/api')

DEFAULT_EMPTY = '--EMPTY--'
IPTV_concurrence_user_num_KEYS = ['id','start_time','end_time','particle_size','element_location','level_first_VOD','level_second_VOD','level_first_LIVE','level_first_TSTV','level_first_TVOD']
BRAS_online_user_num_KEYS = []


"""
@bp.route('/AllFromIPTV_concurrence_user_num/')
@json_resp
def AllFromIPTV_concurrence_user_num():
    result = AllFromTableIPTV_concurrence_user_num()
    return dict(success=True, data=result)

@bp.route('/AllFromBRAS_online_user_num/')
@json_resp
def AllFromBRAS_online_user_num():
    result = AllFromTableBRAS_online_user_num()
    return dict(success=True, data=result)

"""
@bp.route('/AllOfIPTVandBRASRegisterUser/')
@json_resp
def AllOfIPTVandBRASRegisterUser():
    time = request.args.get('time').encode('utf-8')
    if time== None or time == '':
        return dict(success=False,msg="error parameter." )
    else:
        resultIPTV = DateAndNumFromTableIPTV_concurrence_user_num(time)
        resultBRAS = DateAndNumFromTableBRAS_online_user_num(time)
        dic=packagingRegisterUserReturnType(resultIPTV,resultBRAS)
        print(dic)
        return dict(success=True, data=dic)


@bp.route('/AllFromBRASUserNum/')
@json_resp
def AllFromBRASUserNum():
    time = request.args.get('time').encode('utf-8')
    if time== None or time == '':
        return dict(success=False,msg="error parameter." )
    else:
        dic = AllFromTableBRASUserNum(time)
    return dict(success=True, data=dic)

@bp.route('/calculateParametersWithIPTVAndBRAS/')
@json_resp
def CalculateParametersWithIPTVAndBRAS():
    time = request.args.get('time').encode('utf-8')
    if time== None or time == '':
        return dict(success=False,msg="error parameter." )
    else:
        dic = calculateParametersWithIPTVAndBRAS(time)
    return dict(success=True, data=dic)

@bp.route('/all_station/')
@json_resp
def Allstation():
    result = AllfromTableStation()
    return dict(success=True, data=result)

@bp.route('/alldevicesByIdLevelOne/')
@json_resp
def AllDeviceById():
    id = request.args.get('station').encode('utf-8')
    result = AllDevicesByStationId(id)
    return dict(success=True, data=result)

@bp.route('/showInformationOfDevice/')
@json_resp
def ShowInfomationOfDevice():
    """
    type = request.args.get('type').encode('utf-8')
    if type!= "OLT":
        return dict(success=False, msg='only OLT type is allowed to query.')
    :return:
    """
    id = request.args.get('id').encode('utf-8')

    result = ShowInfomationOfDeviceByIdAndType(id)
    return dict(success=True, data=result)







