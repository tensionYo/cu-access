# -*- coding: utf-8 -*-
from flask import Blueprint, request,Response
from flask_login import login_required
from utils.decorator import json_resp, admin_role
from task2_service import  *
from blueprint.clusterimpl import *


bp = Blueprint('task_cluster', __name__, url_prefix='/api')

@bp.route('/cluster/')
def cluster():
    area1 = request.args.get('area1', None).encode('utf-8')
    area2 = request.args.get('area2', None).encode('utf-8')
    group_count = int(request.args.get('group_count', None).encode('utf-8'))
    list1 = area1.split(',')
    list2 = area2.split(',')
    area1_list = []
    area2_list = []
    for i in list1:
        if i != '':
            area1_list.append(int(i))
    for i in list2:
        if i != '':
            area2_list.append(int(i))
    print(area1_list)
    print(area2_list)
    print(group_count)
    return cluster_impl(area1_list,area2_list,group_count)

@bp.route('/ofc_select_user/')
def show():
    ratio = request.args.get('ratio', None).encode('utf-8')
    return show_user(ratio)

