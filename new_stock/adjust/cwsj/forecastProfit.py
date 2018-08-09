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
      try:
        # row[ADJUST_NAME['ForecastProfit']] = row[ADJUST_NAME['forecastl']]/row[ADJUST_NAME['zgb']]
        data.loc[date, self.key] = row[ADJUST_NAME['forecastl']] / row[ADJUST_NAME['zgb']]
      except KeyError as e:
        print(e)

  # def before(self, data):
  #   # base = data.loc[:, ADJUST_NAME['ForecastProfit']].copy()
  #
  #   data.loc[:, self.key] = np.nan
  #   # print(data.loc[:, ADJUST_NAME['ForecastProfit']])
  #   # diff = base - data.loc[:, ADJUST_NAME['ForecastProfit']]
  #   # print(diff)
  #   pass
  #
  # def check(self, base, result):
  #   def innerCheck(x):
  #     if np.isnan(x):
  #       return True
  #     elif math.fabs(x) < 0.000001:
  #       return True
  #
  #     return False
  #
  #   base = base.loc[:, ADJUST_NAME['ForecastProfit']]
  #   result = result.loc[:, ADJUST_NAME['ForecastProfit']]
  #   print(base)
  #   print(result)
  #   diff = base - result
  #   print(diff)
  #   re = diff.map(innerCheck)
  #   print(re)
  #   return re.all()