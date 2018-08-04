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
import util.utils
import const

priorXQ = util.priorXQuarter
priorQ = util.priorQuarter
nextXQ = util.nextXQuarter

from query import query_adjust_cwsj
from query import query_cwsj

KN = const.CWSJ_KEYWORD.ADJUST_NAME
KEY_NAME = const.CWSJ_KEYWORD.KEY_NAME


class AdjustOP:
  def columns(self):
    return []

  def op(self, data):
    pass


class AdjustLoop:
  def __init__(self):
    self._newColumns = []
    self._opList = []

  def addOP(self, op):
    if isinstance(op, AdjustOP):
      self._newColumns.extend(op.columns())
      self._opList.append(op)

  def loop(self, data: pd.DataFrame):
    df = pd.DataFrame(columns=self._newColumns, index=data.index)
    print(data)
    print(df)
    data.join(df)
    # newDF = pd.DataFrame.merge(data, df)
    for one in self._opList:
      one.op(data)

    return data

  def genResult(self, data):
    tmp = self._newColumns
    tmp.append('_id')
    df = pd.DataFrame(data=data.loc[:, tmp], index=data.index)
    print(df)
    return df


class GenQuarterProfit(AdjustOP):
  def columns(self):
    return [const.CWSJ_KEYWORD.ADJUST_NAME['QuarterProfit']]

  def op(self, data):
    for date, row in data.iterrows():
      profit = row[const.CWSJ_KEYWORD.KEY_NAME['jbmgsy']]
      if util.isSameQuarter(date, util.FirstQuarter):
        data.loc[date, const.CWSJ_KEYWORD.ADJUST_NAME['QuarterProfit']] = profit
      else:
        priorDate = priorQ(date)
        try:
          priorData = data.loc[priorDate]
          try:
            data.loc[date, const.CWSJ_KEYWORD.ADJUST_NAME['QuarterProfit']] = profit - priorData.loc[
              const.CWSJ_KEYWORD.KEY_NAME['jbmgsy']]
          except TypeError as e:
            print(e)
        except KeyError as e:
          print(e)


class GenQuarterProfitRatio(AdjustOP):
  def columns(self):
    return [const.CWSJ_KEYWORD.ADJUST_NAME['QuarterProfitRatio'],
            const.CWSJ_KEYWORD.ADJUST_NAME['HalfYearProfitRatio'],
            const.CWSJ_KEYWORD.ADJUST_NAME['ThreeQuarterProfitRatio']]

  def op(self, data):
    for date, row in data.iterrows():
      if util.isSameQuarter(date, util.FirstQuarter):
        data.loc[date, KN['QuarterProfitRatio']] = 1
      else:
        firstQuarter = util.getFirstQuarter(date)
        try:
          firstData = data.loc[firstQuarter]
          try:
            data.loc[date, KN['QuarterProfitRatio']] = data.loc[date, KN['QuarterProfit']] / \
                                                       firstData.loc[KN['QuarterProfit']]
            if util.isSameQuarter(date, util.FourthQuarter):
              priorDate = priorQ(date)
              priorData = data.loc[priorDate]
              yearProfit = row[KEY_NAME['jbmgsy']]
              threeQuarterProfit = priorData.loc[KEY_NAME['jbmgsy']]
              data.loc[date, KN['ThreeQuarterProfitRatio']] = (
                                                                  yearProfit - threeQuarterProfit) / threeQuarterProfit

              prior2Date = priorXQ(date, 2)
              prior2Data = data.loc[prior2Date]
              halfYearQuarterProfit = prior2Data.loc[KEY_NAME['jbmgsy']]
              if halfYearQuarterProfit > 0:
                data.loc[date, KN['HalfYearProfitRatio']] = (
                                                                yearProfit - halfYearQuarterProfit) / halfYearQuarterProfit
              else:
                data.loc[date, KN['HalfYearProfitRatio']] = 1

          except TypeError as e:
            print(e)
        except KeyError as e:
          print(e)


class GenQuarterForecastGrowthRate(AdjustOP):
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


class GenPerShareProfitForecast(AdjustOP):
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


class GenPerShareProfitForecast(AdjustOP):
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


class GenPerShareProfitForecast2(AdjustOP):
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
  df['_id'] = data['_id']
  df[KN['date']] = data.index
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

  loop = AdjustLoop()
  loop.addOP(GenQuarterProfit())
  loop.addOP(GenQuarterProfitRatio())
  loop.addOP(GenQuarterForecastGrowthRate())
  loop.addOP(GenPerShareProfitForecast2())
  df = loop.loop(baseData)
  df = loop.genResult(df)
  print(df)

  util.saveMongoDB(df, util.genKeyDateFunc(KN['date']), 'stock-adjust', 'cwsj-' + code)


if __name__ == '__main__':
  test('000725')

  pass
