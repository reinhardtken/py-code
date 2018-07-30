#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-07-28 04:28:42
# Project: gpfh

from pyspider.libs.base_handler import *

import time
import json
import collections

import pyquery

import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from pymongo import MongoClient
from pymongo import errors
import fake_spider

KEY = 'var XbnsgnRv'
'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?' \
'type=YJBB20_YJYG' \
'&token=70f12f2f4f091e459a279469fe49eca5' \
'&st=ndate&sr=-1&p=1&ps=30' \
'&js=var%20aUDOBatW={pages:(tp),data:%20(x)}' \
'&filter=(IsLatest=%27T%27)(enddate=^2018-09-30^)' \
'&rt=51098106'
base_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?'
headers = {
    'Host': 'data.eastmoney.com',
    'Referer': 'http://data.eastmoney.com/yjfp/201712.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    # 'X-Requested-With': 'XMLHttpRequest',
}
client = MongoClient()
db = client['stock']

from requests.models import RequestEncodingMixin
encode_params = RequestEncodingMixin._encode_params

{"scode":"002069",
 "sname":"獐子岛",
 "sclx":"深交所中小板",
 "enddate":"2016-03-31T00:00:00",
 "forecastl":"-9230700",
 "forecastt":"-9230700",
 "increasel":"2.03",
 "increaset":"2.03",
 "forecastcontent":"预计2016年1-3月归属于上市公司股东的净利润亏损:923.07万元",
 "changereasondscrpt":"报告期内,公司采取优化组织架构、压缩成本费用、细分拓展市场、强化并提升终端服务能力等措施,并取得了一定成效。预计营业收入保持同比增长的态势、期间费用大幅下降、营业利润已显著改善。但受宏观经济下行、海洋牧场仍处于逐步恢复阶段等因素的影响,预计2016年1季度归属于上市公司股东的净利润仍为亏损。",
 "forecasttype":"减亏",
 "yearearlier":-9421629.23,
 "ndate":"2016-04-30T00:00:00",
 "hymc":"农牧饲渔",
 "zfpx":2.03,
 "jlrpx":-9230700.0,
 "forecast":"unknown",
 "IsLatest":"T"}


ID_NAME = 'scode'
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

NEED_TO_NUMBER = {

    'forecastl': '预计净利润下限',
    'forecastt': '预计净利润上限',
    'increasel': '业绩变动幅度下限',
    'increaset': '业绩变动幅度上限',
    'yearearlier': '上年同期净利润',

}

DATA_SUB = {

    'enddate': '截止日期',
    'ndate': '公告日期',
}


#####################################################


class Handler(fake_spider.FakeSpider):
    crawl_config = {
    }

    # def on_start(self):
    #     self.crawl(self.genURL(), callback=self.processFirstPage)

    class InnerTask():
        def __init__(self, date, getTotalNumber=False):
            self._date = date
            self.collection = db['yjyg-' + date]
            self.getTotalNumber = getTotalNumber

        def dump(self):
            return {'data': self._date, 'getTotalNumber': self.getTotalNumber}

        def load(dict):
            return Handler.InnerTask(dict['data'], dict['getTotalNumber'])

        def genParams(self, page, date):
            params = {
                'type': 'YJBB20_YJYG',
                'token': '70f12f2f4f091e459a279469fe49eca5',
                'st': 'ndate',
                'sr': '-1',
                'p': page,
                'ps': '30',
                'js': 'var aUDOBatW={pages:(tp),data: (x)}',
                'filter': '(IsLatest=\'T\')(enddate=^' + date + '^)',
                'rt': int(time.time()),
            }
            return params

        def genUrl(self, page):
            url = encode_params(self.genParams(page, self._date))
            return base_url + url

        def saveDB(self, data, handler):
            for result in data:
                print(result)
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
        return 'http://data.eastmoney.com/bbsj/201806/yjyg.html'

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

        data_list = response.doc('#date_type')
        # doc = pyquery.PyQuery(response)
        # data_list = doc('#sel_bgq')
        out = data_list.find('option')

        for one in out:
            print(one.text)
            #collection = db['yjyg-' + one.text]
            #collection.drop()
            innerTask = Handler.InnerTask(one.text)

            save = innerTask.dump()
            self.crawl(innerTask.genUrl(1), headers=self.header(), callback=self.processSecondPage, save=save)

    def processSecondPage(self, response):
        if response.ok == False:
            return

        content = response.content[13:]
        print(response.url)
        innerTask = Handler.InnerTask.load(response.save)
        try:
            data = content.decode('utf-8')
            print(data)
            data = data.replace('pages', '"pages"', 1)
            data = data.replace('data', '"data"', 1)
            json_data = json.loads(data)  # , encoding='GB2312')
            results = self.parse_page(json_data, innerTask)
            innerTask.saveDB(results, self)
        except UnicodeDecodeError as e:
            print(e)
        except Exception as e:
            print(e)

    def parse_page(self, json, innerTask):
        if json:
            # if json.get('success') != True:
            #     print('failed !!!!')
            #     return

            total = json.get('pages')
            if innerTask.getTotalNumber == False:
                innerTask.getTotalNumber = True
                if total >= 2:
                    save = innerTask.dump()
                    for i in range(2, total + 1):
                        self.crawl(innerTask.genUrl(i), headers=self.header(), callback=self.processSecondPage,
                                   save=save)

            items = json.get('data')
            for index, item in enumerate(items):
                one_stock = {}
                one_stock['_id'] = item.get(ID_NAME)
                for k, v in KEY_NAME.items():
                    if not k in NEED_TO_NUMBER:
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


if __name__ == '__main__':
    #a = json.loads('{pages:0,data: []}')
    gpfh = Handler()
    gpfh.on_start()
    gpfh.run()