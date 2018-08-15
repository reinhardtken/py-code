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



class GenForecastMidGrowthRate(loop.AdjustOPSimpleColumnCheck):
  @property
  def key(self):
    return ADJUST_NAME['ForecastMidGrowthRate']

  def columns(self):
    return [self.key]

  def baseColumns(self):
    return [self.key]

  def processFirstQuarter(self, data, date, row):
    quarterProfit = row[ADJUST_NAME['QuarterProfit']]
    forecastQuarterProfit = np.nan
    try:
      forecastQuarterProfit = data.loc[nextXQ(date, 1), ADJUST_NAME['ForecastQuarterProfit']]
    except KeyError as e:
      print(e)
    if quarterProfit <= 0:
      if util.isnan(forecastQuarterProfit):
        fq = priorXQ(date, 1)
        sq = priorXQ(date, 3)
        total = data.loc[date:sq, ADJUST_NAME['QuarterProfit']].sum(skipna=False)
        jbmgsy = data.loc[fq, KEY_NAME['jbmgsy']]
        data.loc[date, self.key] = total/jbmgsy - 1
      else:
        # fqp = data.loc[nextXQ(date, 1), ADJUST_NAME['ForecastQuarterProfit']]
        total = data.loc[date:priorXQ(date, 2), ADJUST_NAME['QuarterProfit']].sum(skipna=False)
        jbmgsy = data.loc[priorQ(date), KEY_NAME['jbmgsy']]
        data.loc[date, self.key] = (forecastQuarterProfit+total) / jbmgsy - 1
    else:
      if not util.isnan(forecastQuarterProfit):
        hpr = data.loc[priorQ(date), ADJUST_NAME['HalfYearProfitRatio']]
        # fqp = data.loc[nextXQ(date, 1), ADJUST_NAME['ForecastQuarterProfit']]
        jbmgsy = data.loc[priorQ(date), KEY_NAME['jbmgsy']]
        data.loc[date, self.key] = (forecastQuarterProfit + quarterProfit)*(1+hpr) / jbmgsy - 1
      else:
        total = data.loc[priorXQ(date, 1):priorXQ(date, 3), ADJUST_NAME['QuarterProfitRatio']].sum(skipna=False)
        jbmgsy = data.loc[priorQ(date), KEY_NAME['jbmgsy']]
        data.loc[date, self.key] = (1 + total)*quarterProfit / jbmgsy - 1


  def processFourthQuarter(self, data, date, row):
    data.loc[date, self.key] = row[KEY_NAME['jbmgsy']]/ data.loc[util.priorYear(date), KEY_NAME['jbmgsy']] - 1


  def processThirdQuarter(self, data, date, row):
    fqp = np.nan
    try:
      fqp = data.loc[nextXQ(date, 1), ADJUST_NAME['ForecastQuarterProfit']]
    except KeyError as e:
      print(e)
    profit = row[KEY_NAME['jbmgsy']]
    if not util.isnan(fqp):
      data.loc[date, self.key] = (fqp+profit)/data.loc[priorXQ(date, 3), KEY_NAME['jbmgsy']] - 1
    elif profit < 0:
      data.loc[date, self.key] = (profit+data.loc[priorXQ(date, 3), ADJUST_NAME['QuarterProfit']])/ \
                                 data.loc[priorXQ(date, 3), KEY_NAME['jbmgsy']] - 1
    else:
      data.loc[date, self.key] = profit*(1+data.loc[priorXQ(date, 3), ADJUST_NAME['ThreeQuarterProfitRatio']])/ \
                                 data.loc[priorXQ(date, 3), KEY_NAME['jbmgsy']] - 1

  def processSecondQuarter(self, data, date, row):
    fqp = np.nan
    try:
      fqp = data.loc[nextXQ(date, 1), ADJUST_NAME['ForecastQuarterProfit']]
    except KeyError as e:
      print(e)
    profit = row[KEY_NAME['jbmgsy']]
    if not util.isnan(fqp):
      if profit > 0:
        data.loc[date, self.key] = (fqp+profit)*(1+data.loc[priorXQ(date, 2), ADJUST_NAME['ThreeQuarterProfitRatio']])/ \
                                   data.loc[priorXQ(date, 2), KEY_NAME['jbmgsy']] - 1
      else:
        data.loc[date, self.key] = (fqp + profit + data.loc[priorXQ(date, 2), ADJUST_NAME['QuarterProfit']])/\
                                   data.loc[priorXQ(date, 2), KEY_NAME['jbmgsy']] - 1
    else:
      if profit > 0:
        data.loc[date, self.key] = profit*(1 + data.loc[priorXQ(date, 2), ADJUST_NAME['HalfYearProfitRatio']]) / \
                                   data.loc[priorXQ(date, 2), KEY_NAME['jbmgsy']] - 1
      else:
        data.loc[date, self.key] = (profit + data.loc[priorXQ(date, 2):priorXQ(date, 3), ADJUST_NAME['QuarterProfit']].sum(skipna=False)) / \
                                   data.loc[priorXQ(date, 2), KEY_NAME['jbmgsy']] - 1
  def op(self, data):
    for date, row in data.iterrows():
      try:
        if util.isSameQuarter(date, util.FirstQuarter):
          self.processFirstQuarter(data, date, row)
        elif util.isSameQuarter(date, util.SecondQuarter):
          self.processSecondQuarter(data, date, row)
        elif util.isSameQuarter(date, util.ThirdQuarter):
          self.processThirdQuarter(data, date, row)
        else:
          self.processFourthQuarter(data, date, row)
      except TypeError as e:
        print(e)
      except KeyError as e:
        print(e)
