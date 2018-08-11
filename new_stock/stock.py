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
    self._bdf = None

  @property
  def data(self):
    return self._df

  @property
  def benchmark_data(self):
    return self._bdf

  def loadFile(file):
    def string2Datetime(x):
      return x.to_pydatetime()

    df = pd.read_excel(file)
    df.loc[:, const.CWSJ_KEYWORD.KEY_NAME['date']] = df.loc[:, const.CWSJ_KEYWORD.KEY_NAME['date']].map(string2Datetime)
    df.set_index(const.CWSJ_KEYWORD.KEY_NAME['date'], inplace=True)
    return df

  def load(self, **kwargs):
    if 'file' in kwargs:
      self._df = Stock.loadFile(kwargs['file'])
      return

    if 'cwsj' in kwargs and kwargs['cwsj']:
      self._df = query.query_cwsj.QueryTop(-1, self._code)

    if 'yjyg' in kwargs:
      dates = kwargs['yjyg']
      df = query.query_yjyg.Query(dates, self._code)
      self._df = self._df.join(df, how='outer')

    #sort
    self._df.sort_index(inplace=True, ascending=False)
    #fill na
    try:
      self._df.loc[:, const.CWSJ_KEYWORD.KEY_NAME['zgb']].fillna(method='ffill', inplace=True)
    except KeyError as e:
      print(e)


  def loadBenchmark(self, **kwargs):
    if 'file' in kwargs:
      self._bdf = Stock.loadFile(kwargs['file'])
      return

    if 'cwsj' in kwargs and kwargs['cwsj']:
      self._bdf = query.query_cwsj.QueryTop(-1, self._code)

    if 'yjyg' in kwargs:
      dates = kwargs['yjyg']
      df = query.query_yjyg.Query(dates, self._code)
      self._bdf = self._bdf.join(df)


if __name__ == '__main__':
  s = Stock('002415')
  s.load(cwsj=True, yjyg=['2018-09-30', '2018-06-30', '2018-03-31'])
  df = s.data
  print(df)
  df.to_excel('/home/ken/workspace/tmp/new-002415.xls')
  pass
