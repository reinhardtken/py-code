#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-07-28 04:28:42
# Project: gpfh

from pyspider.libs.base_handler import *

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
    # 'X-Requested-With': 'XMLHttpRequest',
}
client = MongoClient()
db = client['stock']
collection = db['gpfh2']
max_page = 2
from requests.models import RequestEncodingMixin

encode_params = RequestEncodingMixin._encode_params

KEY_NAME = {

    'Code': '代码',
    'Name': '名称',
    'XJFH': '现金分红',
    'GXL': '股息率',
    'EarningsPerShare': '每股收益(元)',
    'NetAssetsPerShare': '每股净资产(元)',
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


#####################################################

class Handler(BaseHandler):
    crawl_config = {
    }

    def get_page(self, page):
        params = {
            'js': KEY,
            'pagesize': '50',
            'sr': '1',
            'sortType': 'GQDJR',
            'mtk': u'全部股票'.encode('gb2312'),  # %C8%AB%B2%BF%B9%C9%C6%B1',
            'filter': '(ReportingPeriod=^2017-12-31^)',
            'page': page,
            'rt': int(time.time()),
        }

        url = encode_params(params)
        # url = base_url + urlencode(params)
        return base_url + url

    @every(minutes=24 * 60)
    def on_start(self):
        out = []
        for page in range(1, max_page + 1):
            out.append(self.get_page(page))
        self.crawl(out, callback=self.detail_page)

    # @config(age=10 * 24 * 60 * 60)
    # def index_page(self, response):
    #    for each in response.doc('a[href^="http"]').items():
    #        self.crawl(each.attr.href, callback=self.detail_page)

    @config(age=10 * 24 * 60 * 60)
    # @config(priority=2)
    def detail_page(self, response):
        content = response.content[13:]
        try:
            data = content.decode('gb2312')
            json_data = json.loads(data)  # , encoding='GB2312')
            results = self.parse_page(json_data)
            for result in results:
                print(result)
                self.save_to_mongo(result)
        except UnicodeDecodeError as e:
            print(e)
        return result

    def parse_page(self, json):
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

    def save_to_mongo(self, result):
        update_result = collection.update_one({'_id': result['_id']},
                                              {'$set': result})
        if update_result.matched_count == 0:
            try:
                if collection.insert_one(result):
                    print('Saved to Mongo')
            except errors.DuplicateKeyError as e:
                pass
