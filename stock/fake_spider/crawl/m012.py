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


base_url = 'http://dc.xinhua08.com/?'
headers = {
    'Host': 'dc.xinhua08.com',
    'Referer': 'http://dc.xinhua08.com/9/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
client = MongoClient()
db = client['stock']

from requests.models import RequestEncodingMixin
encode_params = RequestEncodingMixin._encode_params


KEY = 'abc'
MX_TYPE = {

    'M0': 11,
    'M1': 10,
    'M2': 9,
}

KEY_NAME = {
    '_id': '月份',
    'data': '同比增幅',
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

    class InnerTask():
        def __init__(self, date, getTotalNumber=False):
            self._date = date
            self.collection = db['gpfh-' + date]
            self.getTotalNumber = getTotalNumber


        def dump(self):
            return {'data': self._date, 'getTotalNumber': self.getTotalNumber}

        def load(dict):
            return Handler.InnerTask(dict['data'], dict['getTotalNumber'])



        def genUrl(self, page):
            url = encode_params(self.genParams(page, self._date))
            return base_url + url



    def genParams(self, type):
        params = {
            'action': 'json',
            'id': type,
            'jsoncallback': KEY,
            '_': int(time.time()),
        }
        return params

    def url(self):
        out = []
        for k,v in MX_TYPE.items():
            url = encode_params(self.genParams(v))
            url = base_url + url
            out.append((url, k))

        return out


    def header(self):
        headers = {
            'Host': 'dc.xinhua08.com',
            'Referer': 'http://dc.xinhua08.com/9/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }
        return headers

    def saveDB(self, data, key):
        collection = db['macro-' + key]
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
        # d = data[0:len(data)-2]
        # d2 = data[1:len(data) - 2]
        # d3 = data[2:len(data) - 2]
        # d4 = data[3:len(data) - 2]
        # d5 = data[4:len(data) - 2]
        #strange...
        data = data[len(KEY)+2:len(data)-2]
        print(data)
        json_data = json.loads(data)
        date = json_data['xAxis']['data']
        m_data = json_data['series'][0]['data']
        if len(date) == len(m_data):
            save = response.save
            self.saveDB(self.genData(date, m_data), save['key'])




    def genData(self, date, m_data):
        size = len(date)
        for i in range(0, size):
            yield {'_id': date[i], KEY_NAME['_id']: date[i], KEY_NAME['data']: m_data[i]}




    def on_message(self, project, msg):
        return msg






if __name__ == '__main__':
    gpfh = Handler()
    gpfh.on_start()
    gpfh.run()