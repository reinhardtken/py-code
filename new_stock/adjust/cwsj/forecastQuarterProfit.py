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
    return ADJUST_NAME['ForecastQuarterProfit']

  def columns(self):
    return [self.key]

  def baseColumns(self):
    return [self.key]

  def op(self, data):
    for date, row in data.iterrows():
      try:
        if util.isSameQuarter(date, util.FirstQuarter):
          data.loc[date, self.key] = row[ADJUST_NAME['ForecastProfit']]
        else:
          data.loc[date, self.key] = row[ADJUST_NAME['ForecastProfit']] -\
            data.loc[priorQ(date), KEY_NAME['jbmgsy']]
      except KeyError as e:
        print(e)

  # def before(self, data):
  #   data.loc[:, self.key] = np.nan
  #   pass
  #
  def check(self, base, result):
    return loop.AdjustOPSimpleColumnCheck.check(self, base, result)