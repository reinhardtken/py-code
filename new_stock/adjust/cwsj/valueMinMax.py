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



class GenValueMinMax(loop.AdjustOPSimpleColumnCheck):
  @property
  def keyMin(self):
    return ADJUST_NAME['ValueMin']

  @property
  def keyMax(self):
    return ADJUST_NAME['ValueMax']

  def columns(self):
    return [self.keyMin, self.keyMax]

  def baseColumns(self):
    return [self.keyMin, self.keyMax]

  def op(self, data):
    for date, row in data.iterrows():
      try:
        data.loc[date, self.keyMin] = row[ADJUST_NAME['ForecastPerShareProfit']] *\
        row[ADJUST_NAME['PEMin']]
        data.loc[date, self.keyMax] = row[ADJUST_NAME['ForecastPerShareProfit']] *\
        row[ADJUST_NAME['PEMax']]
      except TypeError as e:
        print(e)
      except KeyError as e:
        print(e)
