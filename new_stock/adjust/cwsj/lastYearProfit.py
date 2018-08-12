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



class GenLastYearProfit(loop.AdjustOPSimpleColumnCheck):
  @property
  def keyP(self):
    return ADJUST_NAME['LastYearProfit']

  @property
  def keyR(self):
    return ADJUST_NAME['LastYearROE']

  def columns(self):
    return [self.keyP, self.keyR]

  def baseColumns(self):
    return [self.keyP, ]#self.keyR]

  def op(self, data):
    for date, row in data.iterrows():
      try:
        d = util.priorYear(date)
        d = util.getFourthQuarter(d)
        data.loc[date, self.keyP] = data.loc[d, KEY_NAME['jbmgsy']]
        data.loc[date, self.keyR] = data.loc[d, KEY_NAME['jqjzcsyl']]
      except TypeError as e:
        print(e)
      except KeyError as e:
        print(e)
