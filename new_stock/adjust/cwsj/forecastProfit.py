# -*- coding: utf-8 -*-

# sys
import json
import math
# thirdpart
import pandas as pd
import numpy as np

# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import sys
print(sys.path)
import util
import util.utils
import const
import query.query_stock_list as query
import adjust.loop as loop



priorXQ = util.priorXQuarter
priorQ = util.priorQuarter
nextXQ = util.nextXQuarter

KN = const.CWSJ_KEYWORD.ADJUST_NAME
ID_NAME = const.CWSJ_KEYWORD.ID_NAME
KEY_NAME = const.CWSJ_KEYWORD.KEY_NAME
ADJUST_NAME = const.CWSJ_KEYWORD.ADJUST_NAME
MONGODB_ID = const.MONGODB_ID


class GenForecastProfit(loop.AdjustOPSimpleColumnCheck):

  @property
  def key(self):
    return ADJUST_NAME['ForecastProfit']

  def columns(self):
    return [self.key]

  def baseColumns(self):
    return [self.key]

  def op(self, data):
    for date, row in data.iterrows():
      if self.stock.zgb != 0:
        try:
          data.loc[date, self.key] = row[ADJUST_NAME['forecastl']] / self.stock.zgb
        except KeyError as e:
          print(e)
        except TypeError as e:
          print(e)
