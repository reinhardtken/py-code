# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.secondHand.zyShenzhen2


class SpiderGZ(spiders.secondHand.zyShenzhen2.Spider):
    name = 'zy-esf-gz'
    city = '广州'
    allowed_domains = [
      'gz.centanet.com',
                       ]
    start_urls = [
      'https://gz.centanet.com/ershoufang/',
    ]
    head = 'https://gz.centanet.com'
    collectionName = 'guangzhou'