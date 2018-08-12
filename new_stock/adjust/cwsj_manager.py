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
import stock
from query import query_adjust_cwsj
from query import query_cwsj
import mock.cwsj as mock
import adjust.loop as loop
import adjust.cwsj.forecastProfit as forecastProfit
import adjust.cwsj.quarterProfit as quarterProfit
import adjust.cwsj.quarterProfitRatio as quarterProfitRatio
import adjust.cwsj.forecastQuarterProfit as forecastQuarterProfit
import adjust.cwsj.lastYearProfit as lastYearProfit
import adjust.cwsj.forecastMidGrowthRate as forecastMidGrowthRate
import adjust.cwsj.forecastFinalGrowthRate as forecastFinalGrowthRate
import adjust.cwsj.peMinMax as peMinMax
import adjust.cwsj.forecastPerShareProfit as forecastPerShareProfit
import adjust.cwsj.valueMinMax as valueMinMax



priorXQ = util.priorXQuarter
priorQ = util.priorQuarter
nextXQ = util.nextXQuarter

KN = const.CWSJ_KEYWORD.ADJUST_NAME
ID_NAME = const.CWSJ_KEYWORD.ID_NAME
KEY_NAME = const.CWSJ_KEYWORD.KEY_NAME
ADJUST_NAME = const.CWSJ_KEYWORD.ADJUST_NAME
MONGODB_ID = const.MONGODB_ID





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

  # oneLoop = loop.AdjustLoop()
  # oneLoop.addOP(GenQuarterProfit())
  # oneLoop.addOP(GenQuarterProfitRatio())
  # oneLoop.addOP(GenQuarterForecastGrowthRate())
  # oneLoop.addOP(GenPerShareProfitForecast2())
  # df = oneLoop.loop(baseData)
  # df = oneLoop.genResult(df)
  # print(df)

  util.saveMongoDB(df, util.genKeyDateFunc(KN['date']), 'stock-adjust', 'cwsj-' + code)



def test2(code):
  # df = mock.mock000725()
  # s = stock.Stock('002415')
  # s.load(file='/home/ken/workspace/tmp/im_out-adjust-000725(12).xlsx')
  # df = s.data

  s = stock.Stock('002415')
  s.load(cwsj=None, yjyg=['2018-09-30', '2018-06-30', '2018-03-31'])
  s.loadBenchmark(file='/home/ken/workspace/tmp/out-adjust-002415.xlsx')
  df = s.data
  # df = df.loc[:, [KN['date'], KN['zgb'], KN['jbmgsy']]]
  bdf = s.benchmark_data
  df.to_excel('/home/ken/workspace/tmp/base-002415.xls')

  oneLoop = loop.AdjustLoop()
  oneLoop.addOP(forecastProfit.GenForecastProfit())
  oneLoop.addOP(quarterProfit.GenQuarterProfit())
  oneLoop.addOP(quarterProfitRatio.GenQuarterProfitRatio())
  oneLoop.addOP(forecastQuarterProfit.GenForecastProfit())
  oneLoop.addOP(lastYearProfit.GenLastYearProfit())
  oneLoop.addOP(forecastMidGrowthRate.GenForecastMidGrowthRate())
  oneLoop.addOP(forecastFinalGrowthRate.GenForecastFinalGrowthRate())
  oneLoop.addOP(peMinMax.GenPEMinMax())
  oneLoop.addOP(forecastPerShareProfit.GenForecastPerShareProfit())
  oneLoop.addOP(valueMinMax.GenValueMinMax())
  c = oneLoop.columns
  # df = oneLoop.loop(df)
  # oneLoop.columns.extend([KEY_NAME['jbmgsy'], ADJUST_NAME['zgb'], const.YJYG_KEYWORD.KEY_NAME['forecastl']])
  # column = oneLoop.columns
  # re = df.loc[:, column]
  # re.to_excel('/home/ken/workspace/tmp/out-002415.xls')
  oneLoop.verify(df, bdf)


def calcOne(code, saveDB=True, saveFile=False, benchmark=False):
  print('calcOne %s'%(code))
  s = stock.Stock(code)
  s.load(cwsj=True, yjyg=['2018-09-30', '2018-06-30', '2018-03-31'])
  if benchmark:
    s.loadBenchmark(file='/home/ken/workspace/tmp/out-adjust-' + code + '.xlsx')
  df = s.data
  # df = df.loc[:, [KN['date'], KN['zgb'], KN['jbmgsy']]]
  bdf = s.benchmark_data
  # df.to_excel('/home/ken/workspace/tmp/stock.xls')

  oneLoop = loop.AdjustLoop()
  oneLoop.addOP(forecastProfit.GenForecastProfit(code))
  oneLoop.addOP(quarterProfit.GenQuarterProfit())
  oneLoop.addOP(quarterProfitRatio.GenQuarterProfitRatio())
  oneLoop.addOP(forecastQuarterProfit.GenForecastProfit())
  oneLoop.addOP(lastYearProfit.GenLastYearProfit())
  oneLoop.addOP(forecastMidGrowthRate.GenForecastMidGrowthRate())
  oneLoop.addOP(forecastFinalGrowthRate.GenForecastFinalGrowthRate())
  oneLoop.addOP(peMinMax.GenPEMinMax())
  oneLoop.addOP(forecastPerShareProfit.GenForecastPerShareProfit())
  oneLoop.addOP(valueMinMax.GenValueMinMax())
  # c = oneLoop.columns
  # df = oneLoop.loop(df)
  # oneLoop.columns.extend([KEY_NAME['jbmgsy'], ADJUST_NAME['zgb'], const.YJYG_KEYWORD.KEY_NAME['forecastl']])
  # column = oneLoop.columns
  # re = df.loc[:, column]
  # re.to_excel('/home/ken/workspace/tmp/out-002415.xls')
  dfOut = None
  if benchmark:
    oneLoop.verify(df, bdf)
  else:
    dfOut = oneLoop.loop(df)

  c = oneLoop.columns
  # c.extend([KEY_NAME['date'], KEY_NAME['jbmgsy'], ADJUST_NAME['zgb'], const.YJYG_KEYWORD.KEY_NAME['forecastl']])
  if saveDB:
    dfOut = oneLoop.genResult(dfOut, [KEY_NAME['jbmgsy'], ADJUST_NAME['zgb'], const.YJYG_KEYWORD.KEY_NAME['forecastl']])
    #
    util.saveMongoDB(dfOut, util.genKeyDateFunc(const.MONGODB_ID), 'stock-out', 'cwsj-' + code)

  if saveFile:
    dfOut.to_excel('/home/ken/workspace/tmp/out-' + code + '.xls')


if __name__ == '__main__':
  calcOne('002415', True, False, True)
  for one in const.STOCK_LIST:
    calcOne(one)

  pass
