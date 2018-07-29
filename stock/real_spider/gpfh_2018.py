#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-07-28 08:49:54
# Project: gpfh4

import time
import json
import collections

import pyquery

import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from pymongo import MongoClient
from pymongo import errors

from pyspider.libs.base_handler import *

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
collection = db['gpfh3']
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

DATA_SUB = {
    'YAGGR': 1,
    'GQDJR': 1,
    'CQCXR': 1,
    'ReportingPeriod': 1,
    'ResultsbyDate': 1,
    'NoticeDate': 1,
}

GLOBAL_DIC = {}


#####################################################


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.url(), headers=self.header(), callback=self.processFirstPage)

    # @config(age=10 * 24 * 60 * 60)
    # def index_page(self, response):
    #    for each in response.doc('a[href^="http"]').items():
    #        self.crawl(each.attr.href, callback=self.detail_page)

    class InnerTask():
        def __init__(self, date, getTotalNumber=False):
            self._date = date
            self.collection = db['gpfh-' + date]
            self.getTotalNumber = getTotalNumber

        def dump(self):
            return {'data': self._date, 'getTotalNumber': self.getTotalNumber}

        def load(dict):
            return Handler.InnerTask(dict['data'], dict['getTotalNumber'])

        def genParams(self, page, date):
            params = {
                'js': KEY,
                'pagesize': '50',
                'sr': '-1',
                'sortType': 'GQDJR',
                'mtk': u'全部股票'.encode('gb2312'),  # %C8%AB%B2%BF%B9%C9%C6%B1',
                'filter': '(ReportingPeriod=^' + date + '^)',  # '2017-12-31^)',
                'page': page,
                'rt': int(time.time()),
            }
            return params

        def genUrl(self, page):
            url = encode_params(self.genParams(page, self._date))
            return base_url + url

        def saveDB(self, data, handler, url):
            for result in data:
                # print(result)
                handler.send_message(handler.project_name, result, self._date + '_' + result['_id'])
                update_result = self.collection.update_one({'_id': result['_id']},
                                                           {'$set': result})
                if update_result.matched_count == 0:
                    try:
                        if self.collection.insert_one(result):
                            print('Saved to Mongo')
                    except errors.DuplicateKeyError as e:
                        pass

    def url(self):
        return 'http://data.eastmoney.com/yjfp/201712.html'

    def header(self):
        headers = {
            'Host': 'data.eastmoney.com',
            'Referer': 'http://data.eastmoney.com/yjfp/201712.html',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }
        return headers

    def processFirstPage(self, response):
        if response.ok == False:
            return

        data_list = response.doc('#sel_bgq')
        # doc = pyquery.PyQuery(response)
        # data_list = doc('#sel_bgq')
        out = data_list.find('option')

        for one in out:
            if one.text.startswith('2018'):
                print(one.text)
                innerTask = Handler.InnerTask(one.text)
                save = innerTask.dump()
                self.crawl(innerTask.genUrl(1), headers=self.header(), callback=self.processSecondPage, save=save)

    def processThirdPage(self, response):
        return self.processSecondPage(response)

    def processSecondPage(self, response):
        if response.ok == False:
            return

        content = response.content[13:]
        innerTask = Handler.InnerTask.load(response.save)
        try:
            data = content.decode('gb2312')
            json_data = json.loads(data)  # , encoding='GB2312')
            results = self.parse_page(json_data, innerTask)
            innerTask.saveDB(results, self, response.url)
        except UnicodeDecodeError as e:
            print(e)

    def parse_page(self, json, innerTask):
        if json:
            if json.get('success') != True:
                print('failed !!!!')
                return

            total = json.get('pages')
            if innerTask.getTotalNumber == False:
                innerTask.getTotalNumber = True
                if total >= 2:
                    save = innerTask.dump()
                    for i in range(2, total + 1):
                        print(innerTask.genUrl(i))
                        self.crawl(innerTask.genUrl(i), headers=self.header(), callback=self.processThirdPage,
                                   save=save)

            items = json.get('data')
            for index, item in enumerate(items):
                one_stock = {}
                one_stock['_id'] = item.get('Code')
                for k, v in KEY_NAME.items():
                    if NEED_TO_NUMBER[k] == False:
                        if k in DATA_SUB:
                            one_stock[v] = item.get(k)[:10]
                        else:
                            one_stock[v] = item.get(k)
                    else:
                        try:
                            one_stock[v] = float(item.get(k))
                        except ValueError as e:
                            one_stock[v] = item.get(k)
                yield one_stock

    def on_message(self, project, msg):
        return msg




