# -*- coding: utf-8 -*-

# sys
import json

# thirdpart
import pandas as pd
# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils as utils
import const
from query import query_adjust_cwsj
from query import query_cwsj
import mock.cwsj as mock
import adjust.loop as loop
import adjust.cwsj.forecastProfit as forecastProfit
import adjust.cwsj.quarterProfit as quarterProfit
import adjust.cwsj.quarterProfitRatio as quarterProfitRatio


priorXQ = util.priorXQuarter
priorQ = util.priorQuarter
nextXQ = util.nextXQuarter

KN = const.CWSJ_KEYWORD.ADJUST_NAME
ID_NAME = const.CWSJ_KEYWORD.ID_NAME
KEY_NAME = const.CWSJ_KEYWORD.KEY_NAME
MONGODB_ID = const.MONGODB_ID




class GenQuarterForecastGrowthRate(loop.AdjustOP):
  def columns(self):
    return [const.CWSJ_KEYWORD.ADJUST_NAME['ForecastGrowthRate']]

  def op(self, data):
    for date, row in data.iterrows():
      profit = row[KEY_NAME['jbmgsy']]
      try:
        if util.isSameQuarter(date, util.FirstQuarter):
          priorDateBegin = priorQ(date)
          priorDateEnd = priorXQ(date, 3)
          priorData = data.loc[priorDateBegin:priorDateEnd]
          last4thQuarter = priorData.loc[priorDateBegin, KN['QuarterProfitRatio']]
          last3thQuarter = priorData.loc[priorXQ(date, 2), KN['QuarterProfitRatio']]
          last2thQuarter = priorData.loc[priorDateEnd, KN['QuarterProfitRatio']]
          forecast = ((profit + profit * last4thQuarter + \
                       profit * last3thQuarter + \
                       profit * last2thQuarter) / data.loc[
                        priorQ(date), KEY_NAME['jbmgsy']]) - 1

          data.loc[date, KN['ForecastGrowthRate']] = forecast

        elif util.isSameQuarter(date, util.SecondQuarter):
          last4thQuarter = data.loc[priorXQ(date, 2)]
          forecast = ((profit + profit * last4thQuarter.loc[KN['HalfYearProfitRatio']]) \
                      / data.loc[priorXQ(date, 2), KEY_NAME['jbmgsy']]) - 1
          data.loc[date, KN['ForecastGrowthRate']] = forecast

        elif util.isSameQuarter(date, util.ThirdQuarter):
          last4thQuarter = data.loc[priorXQ(date, 3)]
          forecast = ((profit + profit * last4thQuarter.loc[KN['ThreeQuarterProfitRatio']]) \
                      / data.loc[priorXQ(date, 3), KEY_NAME['jbmgsy']]) - 1

          data.loc[date, KN['ForecastGrowthRate']] = forecast

        else:
          forecast = (profit / data.loc[priorXQ(date, 4), KEY_NAME['jbmgsy']]) - 1
          data.loc[date, KN['ForecastGrowthRate']] = forecast
      except KeyError as e:
        print(e)


class GenPerShareProfitForecast(loop.AdjustOP):
  def columns(self):
    return [const.CWSJ_KEYWORD.ADJUST_NAME['PerShareProfitForecast']]

  def op(self, data):
    for date, row in data.iterrows():
      try:
        if util.isSameQuarter(date, util.FirstQuarter):
          ratio1 = data.loc[priorQ(date), KN['QuarterProfitRatio']]
          ratio2 = data.loc[priorXQ(date, 2), KN['QuarterProfitRatio']]
          ratio3 = data.loc[priorXQ(date, 3), KN['QuarterProfitRatio']]
          data.loc[date, KN['PerShareProfitForecast']] = row.loc[KN['QuarterProfit']] * \
                                                         (1 + ratio1 + ratio2 + ratio3)
          # data.loc[date, KN['QuarterProfitRatio']] = 1
        elif util.isSameQuarter(date, util.SecondQuarter):
          ratio = data.loc[priorXQ(date, 2), KN['HalfYearProfitRatio']]
          data.loc[date, KN['PerShareProfitForecast']] = data.loc[date, KEY_NAME['jbmgsy']] * (
              1 + ratio)
        elif util.isSameQuarter(date, util.ThirdQuarter):
          ratio = data.loc[priorXQ(date, 3), KN['ThreeQuarterProfitRatio']]
          data.loc[date, KN['PerShareProfitForecast']] = data.loc[date, KEY_NAME['jbmgsy']] * (
              1 + ratio)
        else:
          data.loc[date, KN['PerShareProfitForecast']] = data.loc[date, KEY_NAME['jbmgsy']]

      except KeyError as e:
        print(e)


class GenPerShareProfitForecast(loop.AdjustOP):
  def columns(self):
    return [const.CWSJ_KEYWORD.ADJUST_NAME['PerShareProfitForecast']]

  def op(self, data):
    key = KN['PerShareProfitForecast']
    for date, row in data.iterrows():
      try:
        if util.isSameQuarter(date, util.FirstQuarter):
          ratio1 = data.loc[priorQ(date), KN['QuarterProfitRatio']]
          ratio2 = data.loc[priorXQ(date, 2), KN['QuarterProfitRatio']]
          ratio3 = data.loc[priorXQ(date, 3), KN['QuarterProfitRatio']]
          data.loc[date, key] = row.loc[KN['QuarterProfit']] * \
                                (1 + ratio1 + ratio2 + ratio3)
          # data.loc[date, KN['QuarterProfitRatio']] = 1
        elif util.isSameQuarter(date, util.SecondQuarter):
          ratio = data.loc[priorXQ(date, 2), KN['HalfYearProfitRatio']]
          data.loc[date, key] = data.loc[date, KEY_NAME['jbmgsy']] * (
              1 + ratio)
        elif util.isSameQuarter(date, util.ThirdQuarter):
          ratio = data.loc[priorXQ(date, 3), KN['ThreeQuarterProfitRatio']]
          data.loc[date, key] = data.loc[date, KEY_NAME['jbmgsy']] * (
              1 + ratio)
        else:
          data.loc[date, key] = data.loc[date, KEY_NAME['jbmgsy']]

      except KeyError as e:
        print(e)


class GenPerShareProfitForecast2(loop.AdjustOP):
  def __init__(self):
    import mock.yjyg
    self.yjyg = mock.yjyg.mock000725()

  def forecastProfit(self, date):
    try:
      one = self.yjyg.loc[date]
      return one['forecastQuarter']
    except KeyError as e:
      return None

  def columns(self):
    return [const.CWSJ_KEYWORD.ADJUST_NAME['PerShareProfitForecast']]

  def op(self, data):
    key = KN['PerShareProfitForecast']
    for date, row in data.iterrows():
      try:
        if util.isSameQuarter(date, util.FirstQuarter):
          profit = row.loc[KN['QuarterProfit']]
          forecaastProfit = self.forecastProfit(nextXQ(date, 1))
          if profit < 0 and forecaastProfit is None:
            data.loc[date, key] = \
              profit + data.loc[priorXQ(date, 1), KN['QuarterProfit']] \
              + data.loc[priorXQ(date, 2), KN['QuarterProfit']] \
              + data.loc[priorXQ(date, 3), KN['QuarterProfit']]
          elif profit < 0 and forecaastProfit is not None:
            data.loc[date, key] = \
              profit + forecaastProfit \
              + data.loc[priorXQ(date, 2), KN['QuarterProfit']] \
              + data.loc[priorXQ(date, 3), KN['QuarterProfit']]
          elif profit > 0 and forecaastProfit is not None:
            data.loc[date, key] = (profit + forecaastProfit) * (1 + \
                                                                data.loc[priorXQ(date, 1), KN['HalfYearProfitRatio']])
          else:
            data.loc[date, key] = \
              profit * (1 + data.loc[priorXQ(date, 1), KN['QuarterProfitRatio']] \
                        + data.loc[priorXQ(date, 2), KN['QuarterProfitRatio']] \
                        + data.loc[priorXQ(date, 3), KN['QuarterProfitRatio']])
        elif util.isSameQuarter(date, util.SecondQuarter):
          profit = row.loc[KEY_NAME['jbmgsy']]
          forecaastProfit = self.forecastProfit(nextXQ(date, 1))
          if profit > 0 and forecaastProfit is not None:
            data.loc[date, key] = (profit + forecaastProfit) * (
                  1 + data.loc[priorXQ(date, 2), KN['ThreeQuarterProfitRatio']])
          elif profit < 0 and forecaastProfit is not None:
            data.loc[date, key] = profit + forecaastProfit + data.loc[priorXQ(date, 2), KN['QuarterProfit']]
          elif profit > 0 and forecaastProfit is None:
            data.loc[date, key] = profit * (1 + data.loc[
              priorXQ(date, 2), KN['HalfYearProfitRatio']])
          else:
            data.loc[date, key] = profit + data.loc[priorXQ(date, 2), KN['QuarterProfit']] \
                                  + data.loc[priorXQ(date, 3), KN['QuarterProfit']]
        elif util.isSameQuarter(date, util.ThirdQuarter):
          profit = row.loc[KEY_NAME['jbmgsy']]
          forecaastProfit = self.forecastProfit(nextXQ(date, 1))
          if forecaastProfit is not None:
            data.loc[date, key] = profit + forecaastProfit
          elif profit < 0:
            data.loc[date, key] = profit + data.loc[priorXQ(date, 3), KN['QuarterProfit']]
          else:
            data.loc[date, key] = profit * (1 + data.loc[priorXQ(date, 3), KN['ThreeQuarterProfitRatio']])

        else:
          data.loc[date, key] = row[KEY_NAME['jbmgsy']]
      except KeyError as e:
        print(e)


#####################################################################################3


def prepareResult(data):
  df = pd.DataFrame(columns=KN.values())
  df[MONGODB_ID] = data[MONGODB_ID]
  df[KN[ID_NAME]] = data.index
  df.set_index(KN['date'], inplace=True)
  return df


def test(code):
  baseData = query_cwsj.QueryTop(-1, code)
  adjustData = query_adjust_cwsj.QueryTop(-1, code)
  print(baseData)

  if adjustData is None:
    adjustData = prepareResult(baseData)
  print(adjustData)
  # tmp = datetime.datetime.strptime('2018-03-31', '%Y-%m-%d')
  # tmp2 = datetime.datetime.strptime('2018-03-30', '%Y-%m-%d')
  # tmp3 = datetime.datetime.strptime('2017-03-31', '%Y-%m-%d')
  # # re = baseData.index.isin([tmp, tmp2, tmp3])
  # # print(re)
  # # print(baseData[re])
  # re = None
  # try:
  #     re = baseData.loc[tmp2]
  # except Exception as e:
  #     print(e)

  oneLoop = loop.AdjustLoop()
  oneLoop.addOP(GenQuarterProfit())
  oneLoop.addOP(GenQuarterProfitRatio())
  oneLoop.addOP(GenQuarterForecastGrowthRate())
  oneLoop.addOP(GenPerShareProfitForecast2())
  df = oneLoop.loop(baseData)
  df = oneLoop.genResult(df)
  print(df)

  util.saveMongoDB(df, util.genKeyDateFunc(KN['date']), 'stock-adjust', 'cwsj-' + code)



def test2(code):
  df = mock.mock000725()
  oneLoop = loop.AdjustLoop()
  oneLoop.addOP(forecastProfit.GenForecastProfit())
  oneLoop.addOP(quarterProfit.GenQuarterProfit())
  oneLoop.addOP(quarterProfitRatio.GenQuarterProfitRatio())
  oneLoop.verify(df)


if __name__ == '__main__':
  test2('000725')

  pass
