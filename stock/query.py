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
collection = db['gpfh-2017-12-31']
max_page = 56


KEY_NAME = {

'Code': '代码',
'Name': '名称',
'XJFH': '现金分红',
'GXL': '股息率',
'EarningsPerShare': '每股收益(元)',
'NetAssetsPerShare': '每股净资产(元)'	,
'MGGJJ': '每股公积金(元)',
'MGWFPLY': '每股未分配利润(元)',
'JLYTBZZ': '净利润同比增长(%)',
'TotalEquity': '总股本(亿）',
'YAGGR': '预案公告日',
'GQDJR': '股权登记日',
'CQCXR': '除权除息日',
'ProjectProgress': '方案进度',
'NoticeDate': '最新公告日期',
'SZZBL': '送转总比例',
'SGBL': '送股比例',
'ZGBL': '转股比例',
'AllocationPlan': '分配方案',

}

def QueryTop(top):
    out = []
    cursor = collection.find().sort('股息率', pymongo.DESCENDING)
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


    workbook.save('/home/ken/workspace/tmp/out-2017-12-31.xls')


if __name__ == '__main__':
    #re = collection.update_one({'_id' : '1234'}, { '$set' :{'_id' : '1234'}})
    re = QueryTop(-1)
    SaveData(re)
    pass