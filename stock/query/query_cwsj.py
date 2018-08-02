# -*- coding: utf-8 -*-

import time
import json

import xlwt
import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import pymongo
from pymongo import MongoClient
from pymongo import errors


client = MongoClient()
db = client['stock']
collection = db['cwsj-000725']



KEY_NAME = {
    "date": "季度",
"jbmgsy": "基本每股收益(元)",
"kfmgsy": "扣非每股收益(元)",
"xsmgsy": "稀释每股收益(元)",
"mgjzc": "每股净资产(元)",
"mggjj": "每股公积金(元)",
"mgwfply": "每股未分配利润(元)",
"mgjyxjl": "每股经营现金流(元)",
"yyzsr": "营业总收入(元)",
"mlr": "毛利润(元)",
"gsjlr": "归属净利润(元)",
"kfjlr": "扣非净利润(元)",
"yyzsrtbzz": "营业总收入同比增长(%)",
"gsjlrtbzz": "归属净利润同比增长(%)",
"kfjlrtbzz": "扣非净利润同比增长(%)",
"yyzsrgdhbzz": "营业总收入滚动环比增长(%)",
"gsjlrgdhbzz": "归属净利润滚动环比增长(%)",
"kfjlrgdhbzz": "扣非净利润滚动环比增长(%)",
"jqjzcsyl": "加权净资产收益率(%)",
"tbjzcsyl": "摊薄净资产收益率(%)",
"tbzzcsyl": "摊薄总资产收益率(%)",
"mll": "毛利率(%)",
"jll": "净利率(%)",
"sjsl": "实际税率(%)",
"yskyysr": "预收款/营业收入",
"xsxjlyysr": "销售现金流/营业收入",
"jyxjlyysr": "经营现金流/营业收入",
"zzczzy": "总资产周转率(次)",
"yszkzzts": "应收账款周转天数(天)",
"chzzts": "存货周转天数(天)",
"zcfzl": "资产负债率(%)",
"ldzczfz": "流动负债/总负债(%)",
"ldbl": "流动比率",
"sdbl": "速动比率"}

def QueryTop(top):
    out = []
    cursor = collection.find()
    index = 0
    for c in cursor:
        out.append(c)
        print(c)
        index += 1
        if top != -1 and index > top:
            break

    return out


def SaveData(data):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet', cell_overwrite_ok=True)

    index = 0
    for k, v in KEY_NAME.items():
        sheet.write(0, index, v)
        index += 1

    # 获取并写入数据段信息
    row = 0
    for d in data:
        row += 1
        col = 0
        for k, v in KEY_NAME.items():
            sheet.write(row, col, d.get(v))
            col += 1


    workbook.save('/home/ken/workspace/tmp/out-000725.xls')


if __name__ == '__main__':
    #re = collection.update_one({'_id' : '1234'}, { '$set' :{'_id' : '1234'}})
    re = QueryTop(-1)
    SaveData(re)
    pass