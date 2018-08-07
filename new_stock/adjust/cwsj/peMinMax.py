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



class GenPEMinMax(loop.AdjustOPSimpleColumnCheck):
  @property
  def keyMin(self):
    return ADJUST_NAME['PEMin']

  @property
  def keyMax(self):
    return ADJUST_NAME['PEMax']

  def columns(self):
    return [self.keyMin, self.keyMax]

  def baseColumns(self):
    return [self.keyMin, self.keyMax]

  def op(self, data):
    for date, row in data.iterrows():
      try:
        fmg = row[ADJUST_NAME['ForecastMidGrowthRate']]
        if not util.isnan(fmg):
          if fmg > 0:
            data.loc[date, self.keyMin] = 80 * fmg
            data.loc[date, self.keyMax] = 150 * fmg
          else:
            data.loc[date, self.keyMin] = 1
            data.loc[date, self.keyMax] = 0.067 * 100
      except TypeError as e:
        print(e)
      except KeyError as e:
        print(e)
