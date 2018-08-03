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
import pandas as pd
import datetime

client = MongoClient()
db = client['stock']


STOCK_LIST = {
'000725',
"000651",
"002508",
"600566",
"600487",
"300298",
"300642",
"603595",
"603156",
"603868",
"002517",
"603387",
"600690",
"300628",
"002626",
"002294",
"002372",
"002415",
"603516",
"002901",
"000848",
"002032",
"603833",
"603160",
"002304",
"600519",
"300741",
"603288",
}



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

def QueryTop(top, code):
    out = []
    collection = db['cwsj-' + code]
    cursor = collection.find()
    index = 0
    for c in cursor:
        c[KEY_NAME['date']] = datetime.datetime.strptime(c[KEY_NAME['date']], '%Y-%m-%d')
        out.append(c)
        print(c)
        index += 1
        if top != -1 and index > top:
            break

    df = pd.DataFrame(out)
    df.set_index(KEY_NAME['date'], inplace=True)
    return df



def dropAll():
    for one in STOCK_LIST:
        collection = db['cwsj-' + one]
        collection.drop()


if __name__ == '__main__':
    # dropAll()
    df = QueryTop(-1, '000725')
    print(df)
    df.to_excel('/home/ken/workspace/tmp/out-000725.xls')
    # SaveData(re)
    pass