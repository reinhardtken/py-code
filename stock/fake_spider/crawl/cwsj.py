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


base_url = 'http://emweb.securities.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?'

client = MongoClient()
db = client['stock']

from requests.models import RequestEncodingMixin
encode_params = RequestEncodingMixin._encode_params




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

NEED_TO_NUMBER = {

"jbmgsy":"0.2170",
"kfmgsy":"0.1910",
"xsmgsy":"0.2170",
"mgjzc":"2.4372",
"mggjj":"1.1088",
"mgwfply":"0.2985",
"mgjyxjl":"0.7548",
"yyzsr":"938亿",
"mlr":"228亿",
"gsjlr":"75.7亿",
"kfjlr":"66.8亿",
"yyzsrtbzz":"36.15",
"gsjlrtbzz":"301.99",
"kfjlrtbzz":"53185.01",
"yyzsrgdhbzz":"1.45",
"gsjlrgdhbzz":"-7.91",
"kfjlrgdhbzz":"-13.59",
"jqjzcsyl":"9.25",
"tbjzcsyl":"8.92",
"tbzzcsyl":"3.41",
"mll":"25.07",
"jll":"8.38",
"sjsl":"19.31",
"yskyysr":"0.01",
"xsxjlyysr":"1.10",
"jyxjlyysr":"0.28",
"zzczzy":"0.41",
"yszkzzts":"60.84",
"chzzts":"43.00",
"zcfzl":"59.28",
"ldzczfz":"32.76",
"ldbl":"2.01",
"sdbl":"1.83"
}

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
#####################################################





class Handler(fake_spider.FakeSpider):
    crawl_config = {
    }

    def on_start(self):
        out = self.url()
        for one in out:
            save = {'key': one[1]}
            self.crawl(one[0], headers=self.header(), callback=self.processFirstPage, save=save)



    def genParams(self, code):
        def addHead(code):
            if code.startswith('6'):
                return 'SH' + code
            elif code.startswith('0') or code.startswith('3'):
                return 'SZ' + code

        code = addHead(code)
        params = {
            'ctype': 4,
            'type': 0,
            'code': code,# = SZ000725

        }
        return params

    def url(self):



        out = []
        for code in STOCK_LIST:
            url = encode_params(self.genParams(code))
            url = base_url + url
            out.append((url, code))

        return out


    def header(self):
        headers = {
            'Host': 'emweb.securities.eastmoney.com',
            'Referer': 'http://emweb.securities.eastmoney.com/NewFinanceAnalysis/Index?type=web&code=SZ000725',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        return headers

    def saveDB(self, data, key):
        collection = db['cwsj-' + key]
        for result in data:
            print(result)
            self.send_message(self.project_name, result, key + '_' + result['_id'])
            update_result = collection.update_one({'_id': result['_id']},
                                                       {'$set': result})
            if update_result.matched_count == 0:
                try:
                    if collection.insert_one(result):
                        print('Saved to Mongo')
                except errors.DuplicateKeyError as e:
                    pass


    def processFirstPage(self, response):
        if response.ok == False:
            return

        data = response.content.decode('utf-8')
        json_data = json.loads(data)
        result = self.parse_page(json_data)
        save = response.save
        self.saveDB(result, save['key'])





    def parse_page(self, json):
        for item in json:
            one_stock = {}
            one_stock['_id'] = item.get('date')
            for k, v in KEY_NAME.items():
                if not k in NEED_TO_NUMBER:
                    one_stock[v] = item.get(k)
                else:
                    try:
                        one_stock[v] = float(item.get(k))
                    except ValueError as e:
                        try:
                            if item.get(k)[-1] == '亿':#938亿
                                one_stock[v] = float(item.get(k)[:-1]) * 100000000
                        except ValueError as e:
                            one_stock[v] = item.get(k)
            yield one_stock





    def on_message(self, project, msg):
        return msg




def readList():
    import xlrd

    workbook = xlrd.open_workbook('/home/ken/workspace/tmp/in.xlsx')

    sheet = workbook.sheet_by_name('股票池')
    '''
    sheet.nrows　　　　sheet的行数
    sheet.row_values(index)　　　　返回某一行的值列表
　　sheet.row(index)　　　　返回一个row对象，可以通过row[index]来获取这行里的单元格cell对象'''
    nrows = sheet.nrows
    out = []
    for index in range(1, nrows):
        print(nrows)
        row = sheet.row(index)
        out.append(row[0].value)

    for one in out:
        print('"' + str(one) + '",')



if __name__ == '__main__':
    readList()
    gpfh = Handler()
    gpfh.on_start()
    gpfh.run()