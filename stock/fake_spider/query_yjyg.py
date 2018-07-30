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
collection = db['yjyg-2018-09-30']



KEY_NAME = {

    'scode': '代码',
    'sname': '名称',
    'hymc': '板块',
    'enddate': '截止日期',
    'forecastl': '预计净利润下限',
    'forecastt': '预计净利润上限',
    'increasel': '业绩变动幅度下限',
    'increaset': '业绩变动幅度上限',
    'forecastcontent': '业绩变动',
    'changereasondscrpt': '业绩变动原因',
    'forecasttype': '预告类型',
    'yearearlier': '上年同期净利润',
    'ndate': '公告日期',
    'sclx': '市场',
}

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


    workbook.save('/home/ken/workspace/tmp/out-yjyg-2018-09-30.xls')


if __name__ == '__main__':
    #re = collection.update_one({'_id' : '1234'}, { '$set' :{'_id' : '1234'}})
    re = QueryTop(-1)
    SaveData(re)
    pass