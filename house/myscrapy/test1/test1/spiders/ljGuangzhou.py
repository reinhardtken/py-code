# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-gz'
    city = '广州'
    allowed_domains = [
      'gz.lianjia.com',
                       ]
    start_urls = [
      'https://gz.lianjia.com/ershoufang/tianhe/',
    ]
    head = 'https://gz.lianjia.com'
    dbName = 'house'
    collectionName = 'guangzhou'

