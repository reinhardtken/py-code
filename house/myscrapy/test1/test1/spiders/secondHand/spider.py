# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime

import scrapy
from scrapy.http import Request
import numpy as np


import items
import spiders.secondHand.sourceYJ as sourceYJ


def String2Number(s):
  out = np.nan
  try:
    out = float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])
  except Exception as e:
    pass

  return out


def todayString():
  now = datetime.datetime.now()
  now = now.replace(hour=0, minute=0, second=0, microsecond=0)
  return now.strftime('%Y-%m-%d')

def today():
  now = datetime.datetime.now()
  now = now.replace(hour=0, minute=0, second=0, microsecond=0)
  return now


class Spider(scrapy.Spider):
  name = 'all-esf-sh'
  city = '上海'
  dbName = 'house'
  collectionName = 'shanghai'

  allowed_domains = []
  start_urls = []

  sourceList = [
    sourceYJ.SourceYJ(),
  ]

  startURLMap = {}

  def __init__(self):
    for one in self.sourceList:
      self.allowed_domains.extend(one.allowed_domains)
    for one in self.sourceList:
      self.start_urls.extend(one.start_urls)
      for url in one.start_urls:
        self.startURLMap[url] = {}
        self.startURLMap[url]['parse'] = one.parse
        self.startURLMap[url]['anchor'] = one.anchor

    super(Spider, self).__init__()

  def parse(self, response):
    if response.url in self.startURLMap:
      yield from self.startURLMap[response.url]['parse'](response)


  def processAnchor(self, url):
    if url in self.startURLMap:
      return self.startURLMap[url]['anchor']()


