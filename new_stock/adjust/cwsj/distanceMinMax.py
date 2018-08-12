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



class GenDistanceMinMax(loop.AdjustOPSimpleColumnCheck):
  @property
  def keyMin(self):
    return ADJUST_NAME['DistanceMin']

  @property
  def keyMax(self):
    return ADJUST_NAME['DistanceMax']

  def columns(self):
    return [self.keyMin, self.keyMax]

  def baseColumns(self):
    return []

  def op(self, data):
    for date, row in data.iterrows():
      try:
        valueMin = row[ADJUST_NAME['ValueMin']]
        valueMax = row[ADJUST_NAME['ValueMax']]
        if not util.isnan(valueMin):
          data.loc[date, self.keyMin] = (self.stock.lastPrice - valueMin) / valueMin
        if not util.isnan(valueMax):
          data.loc[date, self.keyMax] = (valueMax - self.stock.lastPrice) / self.stock.lastPrice
      except TypeError as e:
        print(e)
      except KeyError as e:
        print(e)
