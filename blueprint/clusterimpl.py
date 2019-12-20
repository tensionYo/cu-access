# -*- coding: utf-8 -*-
from db.client import cli
from flask import Response
from flask import render_template
import base64
import struct
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import csv
from utils.decorator import json_resp, admin_role
import numpy as np
import sklearn
import time
from sklearn.decomposition import PCA
from sklearn import datasets
# 导入内置数据集模块
from sklearn.neighbors import KNeighborsClassifier

# 导入sklearn.neighbors模块中KNN类
from sklearn.cluster import KMeans
@json_resp
def cluster_impl(area1,area2,group_count):
    return_data = {}
    # 判断
    if group_count>6 :
        return dict(success=False, msg='group_count error.')
    if group_count<=0:
        return dict(success=False, msg='group_count error.')
    temp1 = []
    temp2 = []
    if len(area1)!= 0:
        for area1_count in area1:
            sql1 = "select * from cu_ofc where lable = '%s' ;" % area1_count
            res1 = cli.fetchall(sql1)
            for i in res1:
                temp = []
                temp.append(i['increase'])
                temp.append(i['avg_bandwidth'])
                temp1.append(temp)
    data1 = np.array(temp1)

    if len(area2):
        for area2_count in area2:
            sql2 = "select * from cu_ofc where lable = '%s' ;" % area2_count
            res2 = cli.fetchall(sql2)
            for i in res2:
                temp = []
                temp.append(i['increase'])
                temp.append(i['avg_bandwidth'])
                temp2.append(temp)
    data2 = np.array(temp2)
    # 读取文件  读取哪个文件需要进行修改

    #tmp = np.loadtxt('F:\entest.csv', dtype=np.str, delimiter=",")

    # 注：分组数，标签值与颜色个数需要存在一一对应的关系

    # 分组数
    n_clusters = group_count
    # 标签值
    labels = ['Group1', 'Group2', 'Group3', 'Group4', 'Group5', 'Group6'];
    # 颜色
    colors = ['y', 'g', 'r', 'c', 'm', 'black']
    # 图表标题
    strTitle = 'K-means++ Grouping Results in Urban'
    strXlabel = 'Average Traffic (Mbit/s)'  # 第一列的平均带宽
    strYlable = 'Increased Traffic (Mbit/s)'  # 第二列是增长带宽

    if len(temp1)!= 0:
        cls = KMeans(n_clusters, init='k-means++', random_state=1).fit(data1)
        # X中每项所属分类的一个列表

        wdata = cls.labels_  # 每条数据的标签，这是需要的数据，后面可能需要更新到数据库

        ##统计各标签的数据数量
        #每个数据所对应标签所形成的列表的排序列表
        sortedData = sorted(wdata)
        #("sortedData: ", sortedData)  # 数据太大，不输出了
        #标签种类个数列表
        unique_data = np.unique(sortedData)
        unique_data_list = []
        for i in unique_data:
            unique_data_list.append(i)
        print(unique_data_list)
        #每种标签有多少个数
        resdata = []
        for ii in unique_data:
            resdata.append(sortedData.count(ii))
        # 将所有数据按照聚类结果分组返回
        return_list = []
        for i in range(len(unique_data_list)):
            return_list.append([])
        count1 = 0
        for i in wdata:
            return_list[unique_data_list.index(int(i))].append(temp1[count1])
            count1+=1
        for i in range(len(return_list)):
            print(len(return_list[i]))
        return_data['area1'] = return_list

        # 更新分类标签文字
        labels = ['Group1', 'Group2', 'Group3', 'Group4', 'Group5', 'Group6'];
        for lablei in range(n_clusters):
            labels[lablei] = 'Group' + str(lablei) + '  count= ' + str(resdata[lablei])

        ##画图

        markers = ['^', 'x', 'o', '*', '+', '^']
        # col = ['y','g','r','c','m','black']
        col = colors

        # 分n_clusters绘制图形，每次绘制一个分组
        for i in range(n_clusters):
            members = cls.labels_ == i
            plt.scatter(data1[members, 0], data1[members, 1], s=30, c=col[i], alpha=1)
        #print data1[0][0]
        plt.title(strTitle)
        plt.xlabel(strXlabel)
        plt.ylabel(strYlable)
        patches = [mpatches.Patch(color=colors[i], label="{:s}".format(labels[i])) for i in range(n_clusters)]
        ax = plt.gca()
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width, box.height])
        # ax.legend( loc="upper left", handles=patches)
        ax.legend(loc="lower right", handles=patches)  # 放到右上角比较好
        plt.savefig('area11.png')
    if len(temp2)!=0:
        cls = KMeans(n_clusters, init='k-means++', random_state=1).fit(data2)
        # X中每项所属分类的一个列表

        wdata = cls.labels_  # 每条数据的标签，这是需要的数据，后面可能需要更新到数据库

        ##统计各标签的数据数量
        # 每个数据所对应标签所形成的列表的排序列表
        sortedData = sorted(wdata)
        #print("sortedData: ", sortedData)  # 数据太大，不输出了
        # 标签种类个数列表
        unique_data = np.unique(sortedData)
        unique_data_list = []
        for i in unique_data:
            unique_data_list.append(i)
        print(unique_data_list)
        # 每种标签有多少个数
        resdata = []
        for ii in unique_data:
            resdata.append(sortedData.count(ii))
        # 将所有数据按照聚类结果分组返回
        return_list2 = []
        for i in range(len(unique_data_list)):
            return_list2.append([])
        count2 = 0
        for i in wdata:
            return_list2[unique_data_list.index(int(i))].append(temp2[count2])
            count2 += 1
        return_data['area2'] = return_list2


        # 更新分类标签文字
        labels = ['Group1', 'Group2', 'Group3', 'Group4', 'Group5', 'Group6'];
        for lablei in range(n_clusters):
            labels[lablei] = 'Group' + str(lablei) + '  count= ' + str(resdata[lablei])

        ##画图

        markers = ['^', 'x', 'o', '*', '+', '^']
        # col = ['y','g','r','c','m','black']
        col = colors

        # 分n_clusters绘制图形，每次绘制一个分组
        for i in range(n_clusters):
            members = cls.labels_ == i
            plt.scatter(data2[members, 0], data2[members, 1], s=30, c=col[i], alpha=1)
        #print data2[0][0]
        plt.title(strTitle)
        plt.xlabel(strXlabel)
        plt.ylabel(strYlable)
        patches = [mpatches.Patch(color=colors[i], label="{:s}".format(labels[i])) for i in range(n_clusters)]
        ax = plt.gca()
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width, box.height])
        # ax.legend( loc="upper left", handles=patches)
        ax.legend(loc="lower right", handles=patches)  # 放到右上角比较好
        plt.savefig('area22.png')

        return dict(success=True, data=return_data)

    # # 将后台保存的图片返回给前端展示的代码
    # img1_path = 'C:\\Users\\hasee\\PycharmProjects\\jiawu\\cu-access\\area11.png'
    # img1_stream = ''
    # with open(img1_path, 'rb') as img_f:
    #     img1_stream = img_f.read()
    #
    #     img1_stream = base64.b64encode(img1_stream)
    # return render_template('show.html',
    #                        img_stream=img1_stream)

@json_resp
def show_user(ratio):
    if ratio == None:
        return dict(success=False, msg='None params.')
    temp_ratio = ratio.split('%')[0]
    print(type(temp_ratio))
    print(temp_ratio)
    ratio_float = float(temp_ratio)*0.01
    print(ratio_float)
    if 0>ratio_float or ratio_float>1:
        return dict(success=False, msg='error params.')
    sql = "select count(*) as count from cu_ofc_user ;"
    user_num = int(cli.fetchall(sql)[0]['count'])
    select_user_num = int(user_num * ratio_float)
    sql1 = "select * from cu_ofc_user order by total_traffic DESC limit "+str(select_user_num)
    res = cli.fetchall(sql1)
    return_data = []
    count = 0
    for i in res:
        return_data.append(i)
        count+=1
        if count>= select_user_num:
            break
    return dict(success=True, data =return_data)
