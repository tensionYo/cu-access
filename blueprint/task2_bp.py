# -*- coding: utf-8 -*-
from flask import Blueprint, request
from flask_login import login_required
from utils.decorator import json_resp, admin_role
from task2_service import  *


bp = Blueprint('task1_bp', __name__, url_prefix='/api')

DEFAULT_EMPTY = '--EMPTY--'
BUSINESS_PARAMETERS_KEYS = ['type','Resolving_power','Frame_rate','Color_bits','compression_technique','Minimum_rate']
Network_requirements_for_4K_KEYS=['type','bandwidth','time_delay','Packet_loss_rate']
Set_Meal_KEYS=['Set_meal_type','Broadband_commitment_uplink','Broadband_commitment_downlink','IPTV_commitment_uplink','IPTV_commitment_downlink',
               'OLT_uplink_minimum_bandwidth','OLT_uplink_maximum_bandwidth','OLT_downlink_minimum_bandwidth','OLT_downlink_maximum_bandwidth',
               'BRAS_uplink_minimum_bandwidth','BRAS_uplink_maximum_bandwidth','BRAS_downlink_minimum_bandwidth','BRAS_downlink_maximum_bandwidth',
               'Broadband_VLAN','On_demand_VLAN','Live_broadcast_VLAN']
Live_channel_bandwidth_KEYS=['type','channel_num','one_channel_bandwidth_request','total_channel_bandwidth_request']


@bp.route('/AllFromBusiness_parameters/')
@json_resp
def AllFromBusiness_parameters():
    result = AllFromTableBusiness_parameters()
    return dict(success=True, data=result)

@bp.route('/AllFrom4K/')
@json_resp
def AllFrom4K():
    result = ALLFromTable4K()
    return dict(success=True, data=result)

@bp.route('/AllFromSet_Meal/')
@json_resp
def AllFromSet_Meal():
    result = AllFromTableSet_Meal()
    return dict(success=True, data=result)

@bp.route('/AllFromLive_channel_bandwidth/')
@json_resp
def AllFromLive_channel_bandwidth():
    result = AllFromTableLive_channel_bandwidth()
    totalCount = 0
    for k in result:
        if(k['total_channel_bandwidth_request'] != None):
            totalCount+=k['total_channel_bandwidth_request']
    return dict(success=True, data=result,total=totalCount)

@bp.route('/insertIntoBusiness_parameters/')
@json_resp
def InsertIntoBusiness_parameters():
    params = []
    for k in BUSINESS_PARAMETERS_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    InsertIntoTableBusiness_parameters(params)
    result = AllFromTableBusiness_parameters()
    return dict(success=True, data=result)


@bp.route('/insertInto4K/')
@json_resp
def InsertInto4K():
    params = []
    for k in Network_requirements_for_4K_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    InsertIntoTable4K(params)
    result = ALLFromTable4K()
    return dict(success=True, data=result)

@bp.route('/insertIntoSet_Meal/')
@json_resp
def InsertIntoSet_Meal():
    params = []
    for k in Set_Meal_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    InsertIntoTableSet_Meal(params)
    result = AllFromTableSet_Meal()
    return dict(success=True, data=result)

@bp.route('/insertIntoLive_channel_bandwidth/')
@json_resp
def InsertIntoLive_channel_bandwidth():
    params = []
    for k in Live_channel_bandwidth_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    InsertIntoTableLive_channel_bandwidth(params)
    result = AllFromTableLive_channel_bandwidth()
    totalCount = 0
    for k in result:
        if (k['total_channel_bandwidth_request'] != None):
            totalCount += k['total_channel_bandwidth_request']
    return dict(success=True, data=result, total=totalCount)


@bp.route('/deleteFromBusiness_parameters/')
@json_resp
def DeleteFromBusiness_parameters():
    id = request.args.get('id').encode('utf-8')
    DeleteFromTableBusiness_parameters(id)
    result = AllFromTableBusiness_parameters()
    return dict(success=True, data=result)

@bp.route('/deleteFrom4K/')
@json_resp
def DeleteFrom4K():
    id = request.args.get('id').encode('utf-8')
    DeleteFromTable4K(id)
    result = ALLFromTable4K()
    return dict(success=True, data=result)

@bp.route('/deleteFromSet_meal/')
@json_resp
def DeleteFromSet_meal():
    id = request.args.get('id').encode('utf-8')
    DeleteFromTableSet_Meal(id)
    result = AllFromTableSet_Meal()
    return dict(success=True, data=result)

@bp.route('/deleteFromLive_channel_bandwidth/')
@json_resp
def DeleteFromLive_channel_bandwidth():
    id = request.args.get('id').encode('utf-8')
    DeleteFromTableLive_channel_bandwidth(id)
    result = AllFromTableLive_channel_bandwidth()
    totalCount = 0
    for k in result:
        if (k['total_channel_bandwidth_request'] != None):
            totalCount += k['total_channel_bandwidth_request']
    return dict(success=True, data=result, total=totalCount)

@bp.route('/updateFromBusiness_parameters/')
@json_resp
def UpdateFromBusiness_parameters():
    params = []
    for k in BUSINESS_PARAMETERS_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    params.append(request.args.get('id').encode('utf-8'))
    UpdateFromTableBusiness_parameters(params)
    result = AllFromTableBusiness_parameters()
    return dict(success=True, data=result)

@bp.route('/updateFrom4K/')
@json_resp
def UpdateFrom4K():
    params = []
    for k in Network_requirements_for_4K_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    params.append(request.args.get('id').encode('utf-8'))
    UpdateFromTable4K(params)
    result = ALLFromTable4K()
    return dict(success=True, data=result)

@bp.route('/updateFromSet_Meal/')
@json_resp
def UpdateFromSet_Meal():
    params = []
    for k in Set_Meal_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    params.append(request.args.get('id').encode('utf-8'))
    UpdateFromTableSet_Meal(params)
    result = AllFromTableSet_Meal()
    return dict(success=True, data=result)

@bp.route('/updateFromLive_channel_bandwidth/')
@json_resp
def UpdateFromLive_channel_bandwidth():
    params = []
    for k in Live_channel_bandwidth_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    params.append(request.args.get('id').encode('utf-8'))
    UpdateFromTableLive_channel_bandwidth(params)
    result = AllFromTableLive_channel_bandwidth()
    totalCount = 0
    for k in result:
        if (k['total_channel_bandwidth_request'] != None):
            totalCount += k['total_channel_bandwidth_request']
    return dict(success=True, data=result, total=totalCount)
