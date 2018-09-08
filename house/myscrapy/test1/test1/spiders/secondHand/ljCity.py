# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.http import Request
import items
import spiders.ljShanghai


class Spider(spiders.ljShanghai.Spider):
    name = 'lianjia-esf-cs'
    city = '长沙'
    allowed_domains = [
      'cs.lianjia.com',
                       ]
    start_urls = [
      'https://cs.lianjia.com/ershoufang/yuhua/',
    ]
    head = 'https://cs.lianjia.com'
    collectionName = 'changsha'


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-gz'
  city = '广州'
  allowed_domains = [
    'gz.lianjia.com',
  ]
  start_urls = [
    'https://gz.lianjia.com/ershoufang/tianhe/',
  ]
  head = 'https://gz.lianjia.com'
  collectionName = 'guangzhou'

class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-hz'
  city = '杭州'
  allowed_domains = [
    'hz.lianjia.com',
  ]
  start_urls = [
    'https://hz.lianjia.com/ershoufang/xihu/',
  ]
  head = 'https://hz.lianjia.com'
  collectionName = 'hangzhou'


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-hf'
  city = '合肥'
  allowed_domains = [
    'hf.lianjia.com',
  ]
  start_urls = [
    'https://hf.lianjia.com/ershoufang/baohe/',
  ]
  head = 'https://hf.lianjia.com'

  collectionName = 'hefei'

  xpath = spiders.ljShanghai.Spider.xpath
  xpath['districts'] = '/html/body/div[3]/div/div[1]/dl[2]/dd/div/div[1]/a'
  xpath['districtName'] = '/html/body/div[3]/div/div[1]/dl[2]/dd/div/div[1]/a[@class="selected"]/text()'


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-nj'
  city = '南京'
  allowed_domains = [
    'nj.lianjia.com',
  ]
  start_urls = [
    'https://nj.lianjia.com/ershoufang/gulou/',
  ]
  head = 'https://nj.lianjia.com'
  collectionName = 'nanjing'

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


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-su'
  city = '苏州'
  allowed_domains = [
    'su.lianjia.com',
  ]
  start_urls = [
    'https://su.lianjia.com/ershoufang/gongyeyuan/',
  ]
  head = 'https://su.lianjia.com'
  collectionName = 'suzhou'


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-tj'
  city = '天津'
  allowed_domains = [
    'tj.lianjia.com',
  ]
  start_urls = [
    'https://tj.lianjia.com/ershoufang/heping/',
  ]
  head = 'https://tj.lianjia.com'
  collectionName = 'tianjin'


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-wh'
  city = '武汉'
  allowed_domains = [
    'wh.lianjia.com',
  ]
  start_urls = [
    'https://wh.lianjia.com/ershoufang/jiangan/',
  ]
  head = 'https://wh.lianjia.com'
  collectionName = 'wuhan'


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-xm'
  city = '厦门'
  allowed_domains = [
    'xm.lianjia.com',
  ]
  start_urls = [
    'https://xm.lianjia.com/ershoufang/siming/',
  ]
  head = 'https://xm.lianjia.com'

  collectionName = 'xiamen'


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-xa'
  city = '西安'
  allowed_domains = [
    'xa.lianjia.com',
  ]
  start_urls = [
    'https://xa.lianjia.com/ershoufang/beilin/',
  ]
  head = 'https://xa.lianjia.com'
  collectionName = 'xian'


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-zz'
  city = '郑州'
  allowed_domains = [
    'zz.lianjia.com',
  ]
  start_urls = [
    'https://zz.lianjia.com/ershoufang/jinshui/',
  ]
  head = 'https://zz.lianjia.com'

  collectionName = 'zhengzhou'


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-cq'
  city = '重庆'
  allowed_domains = [
    'cq.lianjia.com',
  ]
  start_urls = [
    'https://cq.lianjia.com/ershoufang/jiangbei/',
  ]
  head = 'https://cq.lianjia.com'
  collectionName = 'chongqing'


class Spider(spiders.ljShanghai.Spider):
  name = 'lianjia-esf-cd'
  city = '成都'
  allowed_domains = [
    'cd.lianjia.com',
  ]
  start_urls = [
    'https://cd.lianjia.com/ershoufang/jinjiang/',
  ]
  head = 'https://cd.lianjia.com'
  collectionName = 'chengdu'