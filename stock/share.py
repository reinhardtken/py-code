# -*- coding: utf-8 -*-

import time
import json


import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from pymongo import MongoClient
from pymongo import errors

KEY = 'var XbnsgnRv'
base_url = 'http://data.eastmoney.com/DataCenter_V3/yjfp/getlist.ashx?'
headers = {
    'Host': 'data.eastmoney.com',
    'Referer': 'http://data.eastmoney.com/yjfp/201712.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    #'X-Requested-With': 'XMLHttpRequest',
}
client = MongoClient()
db = client['stock']
collection = db['gpfh']
max_page = 56

'''
    'MarketType' (139822665391600) = {str} '中小板'
'Code' (139822406858040) = {str} '002793'
'Name' (139822406858096) = {str} '东音股份'
'SZZBL' (139822406858152) = {str} '0.0'
'SGBL' (139822406859720) = {str} '-'
'ZGBL' (139822406859552) = {str} '-'
'XJFH' (139822406859832) = {str} '1.0'
'GXL' (139822406859944) = {str} '0.00629722921914358'
'YAGGR' (139822406860000) = {str} '2018-01-30T00:00:00'
'YAGGRHSRZF' (139822407311152) = {str} '-8.344'
'GQDJRQSRZF' (139822407310640) = {str} '9.5172'
'GQDJR' (139822406860168) = {str} '2018-03-09T00:00:00'
'CQCXR' (139822406860224) = {str} '2018-03-12T00:00:00'
'CQCXRHSSRZF' (139822406870896) = {str} '-11.4886'
'YCQTS' (139822406860280) = {str} '135.0'
'TotalEquity' (139822406871152) = {str} '200000000.0'
'EarningsPerShare' (139822406833040) = {str} '0.58'
'NetAssetsPerShare' (139822406833544) = {str} '3.77092645'
'MGGJJ' (139822406860448) = {str} '1.051719'
'MGWFPLY' (139822406860504) = {str} '1.488969'
'JLYTBZZ' (139822406860560) = {str} '15.4329'
'ReportingPeriod' (139822406871600) = {str} '2017-12-31T00:00:00'
'ResultsbyDate' (139822406871664) = {str} '2018-01-30T00:00:00'
'ProjectProgress' (139822406824432) = {str} '实施分配'
'AllocationPlan' (139822406824560) = {str} '10派1.00元(含税,扣税后0.90元)'
'NoticeDate' (139822406824496) = {str} '2018-03-06T00:00:00'
'''
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


NEED_TO_NUMBER = {

'Code': False,
'Name': False,
'XJFH': True,
'GXL': True,
'EarningsPerShare': True,
'NetAssetsPerShare': True,
'MGGJJ': True,
'MGWFPLY': True,
'JLYTBZZ': True,
'TotalEquity': True,
'YAGGR': False,
'GQDJR': False,
'CQCXR': False,
'ProjectProgress': False,
'NoticeDate': False,
'SZZBL': True,
'SGBL': True,
'ZGBL': True,
'AllocationPlan': False,

}

DATA_SUB = {
'YAGGR': 1,
'GQDJR': 1,
'CQCXR': 1,
'ReportingPeriod': 1,
'ResultsbyDate': 1,
'NoticeDate': 1,
}


def get_page(page):
    #getlist.ashx?js=var%20XbnsgnRv&
    # pagesize=50&page=3&sr=1&sortType=GQDJR
    # &mtk=%C8%AB%B2%BF%B9%C9%C6%B1&filter=(ReportingPeriod=^2017-12-31^)
    # &rt=51083811
    params = {
        'js': KEY,
        'pagesize': '50',
        'sr': '1',
        'sortType': 'GQDJR',
        'mtk': u'全部股票'.encode('gb2312'),#%C8%AB%B2%BF%B9%C9%C6%B1',
        'filter': '(ReportingPeriod=^2017-12-31^)',
        'page': page,
        'rt': int(time.time()),
    }
    from requests.models import RequestEncodingMixin
    encode_params = RequestEncodingMixin._encode_params
    tmp = encode_params(params)
    url = base_url + urlencode(params)
    s = requests.Session()
    s.mount('http://', requests.adapters.HTTPAdapter(max_retries=5))
    s.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))
    try:
        response = s.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.content, page
        else:print('net Error', response.status_code)

    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json, page: int):
    if json:
        if json.get('success') != True:
            print('failed !!!!')
            return
        items = json.get('data')
        for index, item in enumerate(items):
            one_stock = {}
            one_stock['_id'] = item.get('Code')
            for k, v in KEY_NAME.items():
                if NEED_TO_NUMBER[k] == False:
                    one_stock[v] = item.get(k)
                else:
                    try:
                        one_stock[v] = float(item.get(k))
                    except ValueError as e:
                        one_stock[v] = item.get(k)
            yield one_stock



def save_to_mongo(result):
    update_result = collection.update_one({'_id': result['_id']},
                                          {'$set': result})
    if update_result.matched_count == 0:
        try:
            if collection.insert_one(result):
                print('Saved to Mongo')
        except errors.DuplicateKeyError as e:
            pass






if __name__ == '__main__':
    for page in range(1, max_page + 1):
        raw_content = get_page(page)
        #data = str(raw_content[0])
        #content = data[data.find(KEY) + len(KEY) + 1:]
        content = raw_content[0][13:]
        try:
            data = content.decode('gb2312')
            json_data = json.loads(data)#, encoding='GB2312')
            results = parse_page(json_data, raw_content[1])
            for result in results:
                print(result)
                save_to_mongo(result)
        except UnicodeDecodeError as e:
            print(e)