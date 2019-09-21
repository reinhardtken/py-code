#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-07-28 04:28:42
# Project: gpfh


# sys
import json
# thirdpart
import pandas as pd
from requests.models import RequestEncodingMixin

encode_params = RequestEncodingMixin._encode_params

# this project
if __name__ == '__main__':
  import sys
  
  sys.path.append('C:/workspace/code/self/github/py-code/ald')

##########################
import util

from spiders import toplist2


class Handler(toplist2.Handler):
  crawl_config = {
  }
  DB_NAME = "ald"
  COLLECTION_NAME = 'camera'
  CHINESE_NAME = '图片摄影'
  post = {
    "type": 0,
    "typeid": 17,
    "date": 1,
    "size": 30,
    "token": "",
  }


def run():
  gpfh = Handler()
  gpfh.on_start()
  gpfh.run()


if __name__ == '__main__':
  gpfh = Handler()
  gpfh.on_start()
  gpfh.run()