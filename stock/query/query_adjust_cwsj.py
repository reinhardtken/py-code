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
db = client['stock-adjust']
collection = db['cwsj-000725']



KN = {
"date": "季度",
'QuarterProfit': '当季每股收益',
'QuarterProfitRatio': '较一季度比例',
'HalfYearProfitRatio': '较上半年比例',
'ThreeQuarterProfitRatio': '较前三季度比例',
'ForecastGrowthRate': '预测增长率',
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
    for k, v in KN.items():
        sheet.write(0, index, v)
        index += 1

    # 获取并写入数据段信息
    row = 0
    for d in data:
        row += 1
        col = 0
        for k, v in KN.items():
            sheet.write(row, col, d.get(v))
            col += 1


    workbook.save('/home/ken/workspace/tmp/out-adjust-000725.xls')


if __name__ == '__main__':
    #re = collection.update_one({'_id' : '1234'}, { '$set' :{'_id' : '1234'}})
    re = QueryTop(-1)
    SaveData(re)
    pass