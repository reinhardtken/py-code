# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-cq'
    allowed_domains = [
      'cq.lianjia.com',
                       ]
    start_urls = [
      'https://cq.lianjia.com/ershoufang/jiangbei/',
    ]
    head = 'https://cq.lianjia.com'
    dbName = 'house'
    collectionName = 'chongqing'

