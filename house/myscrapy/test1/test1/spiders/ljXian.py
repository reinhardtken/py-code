# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-xa'
    allowed_domains = [
      'xa.lianjia.com',
                       ]
    start_urls = [
      'https://xa.lianjia.com/ershoufang/beilin/',
    ]
    head = 'https://xa.lianjia.com'
    dbName = 'house'
    collectionName = 'xian'