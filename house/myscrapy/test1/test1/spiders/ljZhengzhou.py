# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-zz'
    allowed_domains = [
      'zz.lianjia.com',
                       ]
    start_urls = [
      'https://zz.lianjia.com/ershoufang/jinshui/',
    ]
    head = 'https://zz.lianjia.com'
    dbName = 'house'
    collectionName = 'zhengzhou'