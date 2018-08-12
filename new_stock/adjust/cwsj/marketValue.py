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



class GenMarketValue(loop.AdjustOPSimpleColumnCheck):
  @property
  def key(self):
    return ADJUST_NAME['MarketValue']

  def columns(self):
    return [self.key]

  def baseColumns(self):
    return []

  def op(self, data):
    try:
      data.loc[:, self.key] = self.stock.lastPrice * self.stock.zgb
    except TypeError as e:
      print(e)
    except KeyError as e:
      print(e)



class GenZGB(loop.AdjustOPSimpleColumnCheck):
  @property
  def key(self):
    return ADJUST_NAME['zgb']

  def columns(self):
    return [self.key]

  def baseColumns(self):
    return []

  def op(self, data):
    try:
      data.loc[:, self.key] = self.stock.zgb
    except TypeError as e:
      print(e)
    except KeyError as e:
      print(e)


class GenIndustry(loop.AdjustOPSimpleColumnCheck):
  @property
  def key(self):
    return ADJUST_NAME['industry']

  def columns(self):
    return [self.key]

  def baseColumns(self):
    return []

  def op(self, data):
    try:
      data.loc[:, self.key] = self.stock.industry
    except TypeError as e:
      print(e)
    except KeyError as e:
      print(e)
