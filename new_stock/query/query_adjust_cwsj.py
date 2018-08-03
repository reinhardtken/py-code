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
db = client['stock-adjust']


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
'QuarterProfit': '当季每股收益',
'QuarterProfitRatio': '较一季度比例',
'HalfYearProfitRatio': '较上半年比例',
'ThreeQuarterProfitRatio': '较前三季度比例',
'ForecastGrowthRate': '预测增长率',
}

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

    if len(out):
        df = pd.DataFrame(out)
        df.set_index(KEY_NAME['date'], inplace=True)
        return df
    else:
        return None



def dropAll():
    for one in STOCK_LIST:
        collection = db['cwsj-' + one]
        collection.drop()


if __name__ == '__main__':
    # dropAll()
    df = QueryTop(-1, '000725')
    print(df)
    df.to_excel('/home/ken/workspace/tmp/out-adjust-000725.xls')
    # SaveData(re)
    pass