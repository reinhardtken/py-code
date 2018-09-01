# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-hz'
    city = '杭州'
    allowed_domains = [
      'hz.lianjia.com',
                       ]
    start_urls = [
      'https://hz.lianjia.com/ershoufang/xihu/',
    ]
    head = 'https://hz.lianjia.com'

    collectionName = 'hangzhou'

