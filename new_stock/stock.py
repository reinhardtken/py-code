# -*- coding: utf-8 -*-


# sys
import datetime

# thirdpart
import pandas as pd
import pymongo
from pymongo import MongoClient

# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils
import const
import query
import query.query_cwsj
import query.query_yjyg

class Stock:
  def __init__(self, code):
    self._code = code
    self._df = None

  @property
  def data(self):
    return self._df

  def load(self, **kwargs):
    if 'cwsj' in kwargs:
      self._df = query.query_cwsj.QueryTop(-1, self._code)

    if 'yjyg' in kwargs:
      dates = kwargs['yjyg']
      df = query.query_yjyg.Query(dates, self._code)
      self._df = self._df.join(df)


if __name__ == '__main__':
  s = Stock('002415')
  s.load(cwsj=None, yjyg=['2018-09-30', '2018-06-30', '2018-03-31'])
  df = s.data
  print(df)
  df.to_excel('/home/ken/workspace/tmp/new-002415.xls')
  pass
