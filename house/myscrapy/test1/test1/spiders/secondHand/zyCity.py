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


class SpiderNJ(spiders.secondHand.zyShenzhen2.Spider):
  name = 'zy-esf-nj'
  city = '南京'
  allowed_domains = [
    'nj.centanet.com',
  ]
  start_urls = [
    'https://nj.centanet.com/ershoufang/',
  ]
  head = 'https://nj.centanet.com'
  collectionName = 'nanjing'


class SpiderTJ(spiders.secondHand.zyShenzhen2.Spider):
  name = 'zy-esf-tj'
  city = '天津'
  allowed_domains = [
    'tj.centanet.com',
  ]
  start_urls = [
    'https://tj.centanet.com/ershoufang/',
  ]
  head = 'https://tj.centanet.com'
  collectionName = 'tianjin'


class SpiderCD(spiders.secondHand.zyShenzhen2.Spider):
  name = 'zy-esf-cd'
  city = '成都'
  allowed_domains = [
    'cd.centanet.com',
  ]
  start_urls = [
    'https://cd.centanet.com/ershoufang/',
  ]
  head = 'https://cd.centanet.com'
  collectionName = 'chengdu'


class SpiderCQ(spiders.secondHand.zyShenzhen2.Spider):
  name = 'zy-esf-cq'
  city = '重庆'
  allowed_domains = [
    'cq.centanet.com',
  ]
  start_urls = [
    'https://cq.centanet.com/ershoufang/',
  ]
  head = 'https://cq.centanet.com'
  collectionName = 'chongqing'