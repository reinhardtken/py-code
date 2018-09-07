# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-esf-sz'
    city = '深圳'
    allowed_domains = [
      'sz.lianjia.com',
                       ]
    start_urls = [
      'https://sz.lianjia.com/ershoufang/nanshanqu/',
    ]
    head = 'https://sz.lianjia.com'

    collectionName = 'shenzhen'

