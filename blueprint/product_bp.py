# encoding = utf-8
from flask import Blueprint, request
from flask_login import login_required
from utils.decorator import json_resp, admin_role
from blueprint.product_service import *
from task2_service import  *

bp = Blueprint('product_bp', __name__, url_prefix='/product')

DEFAULT_EMPTY = '--EMPTY--'
PRODUCT_KEYS = ['bandwidth', 'delay', 'packet_loss_rate']
BUSINESS_PARAMETERS_KEYS = ['type','Resolving_power','Frame_rate','Color_bits','compression_technique','Minimum_rate']
Network_requirements_for_4K_KEYS=['type','bandwidth','time_delay','Packet_loss_rate']
Set_Meal_KEYS=['Set_meal_type','Broadband_commitment_uplink','Broadband_commitment_downlink','IPTV_commitment_uplink','IPTV_commitment_downlink',
               'OLT_uplink_minimum_bandwidth','OLT_uplink_maximum_bandwidth','OLT_downlink_minimum_bandwidth','OLT_downlink_maximum_bandwidth',
               'BRAS_uplink_minimum_bandwidth','BRAS_uplink_maximum_bandwidth','BRAS_downlink_minimum_bandwidth','BRAS_downlink_maximum_bandwidth',
               'Broadband_VLAN','On_demand_VLAN','Live_broadcast_VLAN']

@bp.route('/create/')
@login_required
@json_resp
@admin_role
def create_product():
    params = []
    for k in PRODUCT_KEYS:
        params.append(request.args.get(k, DEFAULT_EMPTY).encode('utf-8'))
    add_product(params)
    return dict(success=True, data='ok')


@bp.route('/save/')
@login_required
@json_resp
@admin_role
def modify_product():
    return None


