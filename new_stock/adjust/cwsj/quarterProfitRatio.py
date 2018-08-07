# -*- coding: utf-8 -*-

# sys
import json
import math
import datetime
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



class GenQuarterProfitRatio(loop.AdjustOPSimpleColumnCheck):
  @property
  def keyQ(self):
    return ADJUST_NAME['QuarterProfitRatio']

  @property
  def keyH(self):
    return ADJUST_NAME['HalfYearProfitRatio']

  @property
  def keyT(self):
    return ADJUST_NAME['ThreeQuarterProfitRatio']

  def columns(self):
    return [self.keyQ, self.keyH, self.keyT]

  def baseColumns(self):
    return [ADJUST_NAME['jyjdbl_jy'], ADJUST_NAME['jsbnbl_jy'], ADJUST_NAME['jqsjdbl_jy']]

  def bypass(self, data, columns):
    # if len(data.index) == 1:
    #   if data.index[0] == datetime.datetime.strptime('2018-12-31', '%Y-%m-%d'):
    #     if columns[1] == self.keyH or columns[1] == self.keyT:
    #       return True

    return False

  def op(self, data):
    for date, row in data.iterrows():
      if util.isSameQuarter(date, util.FirstQuarter):
        data.loc[date, self.keyQ] = 1
      else:
        firstQuarter = util.getFirstQuarter(date)
        try:
          firstData = data.loc[firstQuarter]
          firstQuarterProfit = firstData.loc[KN['QuarterProfit']]
          try:
            if firstQuarterProfit > 0:
              data.loc[date, self.keyQ] = data.loc[date, KN['QuarterProfit']] / firstQuarterProfit
            else:
              data.loc[date, self.keyQ] = 1
            if util.isSameQuarter(date, util.FourthQuarter):
              priorDate = priorQ(date)
              priorData = data.loc[priorDate]
              yearProfit = row[KEY_NAME['jbmgsy']]
              threeQuarterProfit = priorData.loc[KEY_NAME['jbmgsy']]
              if not util.isnan(threeQuarterProfit):
                if threeQuarterProfit > 0:
                  data.loc[date, self.keyT] = (yearProfit - threeQuarterProfit) / threeQuarterProfit
                else:
                  data.loc[date, self.keyT] = float(1) / float(3)
              prior2Date = priorXQ(date, 2)
              prior2Data = data.loc[prior2Date]
              halfYearQuarterProfit = prior2Data.loc[KEY_NAME['jbmgsy']]
              if not util.isnan(halfYearQuarterProfit):
                if halfYearQuarterProfit > 0:
                  data.loc[date, self.keyH] = (yearProfit - halfYearQuarterProfit) / halfYearQuarterProfit
                else:
                  data.loc[date, self.keyH] = 1

          except TypeError as e:
            print(e)
        except KeyError as e:
          print(e)
