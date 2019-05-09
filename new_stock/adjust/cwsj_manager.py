# -*- coding: utf-8 -*-

# sys
import json
import datetime
# thirdpart
import pandas as pd
import numpy as np
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
import adjust.cwsj.marketValue as marketValue
import adjust.cwsj.forecastPE as forecastPE
import adjust.cwsj.distanceMinMax as distanceMinMax
import setting

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




def test(saveDB=True, saveFile=False, benchmark=False):
  s = stock.Stock('000725')
  mock = {
    'file': setting.PATH + 'im_out-adjust-000725(12).xlsx',
    'zgb': 33862290000,
  }
  s.load(mock=mock)
  df = s.data
  # df = df.loc[:, [KN['date'], KN['zgb'], KN['jbmgsy']]]
  bdf =df.copy()


  oneLoop = loop.AdjustLoop()
  oneLoop.addOP(marketValue.GenMarketValue(s))
  oneLoop.addOP(marketValue.GenZGB(s))
  oneLoop.addOP(marketValue.GenIndustry(s))
  oneLoop.addOP(marketValue.GenLastPrice(s))
  oneLoop.addOP(marketValue.GenCodeAndName(s))
  oneLoop.addOP(forecastProfit.GenForecastProfit(s))
  oneLoop.addOP(quarterProfit.GenQuarterProfit(s))
  oneLoop.addOP(quarterProfitRatio.GenQuarterProfitRatio(s))
  oneLoop.addOP(forecastQuarterProfit.GenForecastProfit(s))
  oneLoop.addOP(lastYearProfit.GenLastYearProfit(s))
  oneLoop.addOP(forecastMidGrowthRate.GenForecastMidGrowthRate(s))
  oneLoop.addOP(forecastFinalGrowthRate.GenForecastFinalGrowthRate(s))
  oneLoop.addOP(peMinMax.GenPEMinMax(s))
  oneLoop.addOP(forecastPerShareProfit.GenForecastPerShareProfit(s))
  oneLoop.addOP(forecastPE.GenForecastPE(s))
  oneLoop.addOP(valueMinMax.GenValueMinMax(s))
  oneLoop.addOP(distanceMinMax.GenDistanceMinMax(s))
  dfOut = oneLoop.verify(df, bdf)




def filterOut(df):
  forecastNow = np.nan
  forecastNext = np.nan
  notNull = df[ADJUST_NAME['ForecastQuarterProfit']].notnull()
  out = df.loc[notNull, :].head(2)

  if len(out.index):
    # 11月1日-4月30：上一年4季
    # 如果是11月15号，有今年四季度的每股收益，则当季是明年一季度。否则，是今年四季度
    # 如果是2月15号，有去年四季度每股收益，则当季是今年一季度，否则是去年四季度
    # 5月1-8月30：二季
    # 9月1-10月30：三季
    r = util.performancePreviewRange()
    try:
      # now = datetime.datetime.now()
      # nowDay = now.replace(hour=0, minute=0, second=0, microsecond=0)
      #
      # lastNovember = now.replace(year=now.year-1, month=11, day=1, hour=0, minute=0, second=0, microsecond=0)
      # nowMay = now.replace(month=5, day=1, hour=0, minute=0, second=0, microsecond=0)
      # nowAugust = now.replace(month=8, day=31, hour=0, minute=0, second=0, microsecond=0)
      # nowOctober = now.replace(month=10, day=30, hour=0, minute=0, second=0, microsecond=0)
      #
      # if (nowDay - lastNovember).total_seconds() >= 0 and (nowDay - nowMay).total_seconds() < 0:
      #   if nowDay.month <= 4:
      #     #看去年四季度是否存在
      #     fq = now.replace(year=now.year-1, month=12, day=31, hour=0, minute=0, second=0, microsecond=0)
      #     try:
      #       tmp = np.nan
      #       tmp = df.loc[fq, KEY_NAME['jbmgsy']]
      #     except KeyError as e:
      #       pass
      #     if np.isnan(tmp):
      #       r = [util.getFourthQuarter(fq), util.getFirstQuarter(nowDay)]
      #     else:
      #       r = [util.getFirstQuarter(nowDay), util.getSecondQuarter(nowDay)]
      #   else:
      #     #此时四季度收益必然不存在
      #     r = [util.getFourthQuarter(nowDay), util.getFirstQuarter(nextXQ(nowDay, 1))]
      # elif (nowDay - nowMay).total_seconds() >= 0 and (nowDay - nowAugust).total_seconds() < 0:
      #   r = [util.getSecondQuarter(nowDay), util.getThirdQuarter(nowDay)]
      # elif (nowDay - nowAugust).total_seconds() >= 0 and (nowDay - nowOctober).total_seconds() < 0:
      #   r = [util.getThirdQuarter(nowDay), util.getFourthQuarter(nowDay)]


      forecastNow = df.loc[r[0], const.YJYG_KEYWORD.KEY_NAME['increasel']]
      forecastNext = df.loc[r[1], const.YJYG_KEYWORD.KEY_NAME['increasel']]
    except KeyError as e:
      print(e)
    pass

  notNull = df[KEY_NAME['jbmgsy']].notnull()
  out = df.loc[notNull, :].head(1)
  out[ADJUST_NAME['ForecastNow']] = forecastNow
  out[ADJUST_NAME['ForecastNext']] = forecastNext
  print(out)
  return out



def changeColumns(df):
  return df[[ADJUST_NAME['code'],
             ADJUST_NAME['name'],
             ADJUST_NAME['ForcastPE'],
             ADJUST_NAME['ForecastNow'],
             ADJUST_NAME['ForecastNext'],
             ADJUST_NAME['DistanceMin'],
             ADJUST_NAME['DistanceMax'],
             ADJUST_NAME['lastPrice'],
             ADJUST_NAME['ValueMin'],
             ADJUST_NAME['ValueMax'],
             ADJUST_NAME['LastYearROE'],
             ADJUST_NAME['LastYearProfit'],
             ADJUST_NAME['ForecastPerShareProfit'],
             ADJUST_NAME['ForecastFinalGrowthRate'],
             ADJUST_NAME['PEMin'],
             ADJUST_NAME['PEMax'],
             ADJUST_NAME['MarketValue'],
             ADJUST_NAME['industry'],
             '_id',
             KEY_NAME['jbmgsy'],
             ]]


def calcOne(code, saveDB=True, saveFile=False, benchmark=False):
  print('calcOne %s'%(code))
  s = stock.Stock(code)
  s.load(cwsj=True, yjyg=setting.yjyg_list)
  if benchmark:
    s.loadBenchmark(file=setting.PATH + 'out-adjust-' + code + '.xlsx')
  df = s.data
  # df = df.loc[:, [KN['date'], KN['zgb'], KN['jbmgsy']]]
  bdf = s.benchmark_data


  oneLoop = loop.AdjustLoop()
  oneLoop.addOP(marketValue.GenMarketValue(s))
  oneLoop.addOP(marketValue.GenZGB(s))
  oneLoop.addOP(marketValue.GenIndustry(s))
  oneLoop.addOP(marketValue.GenLastPrice(s))
  oneLoop.addOP(marketValue.GenCodeAndName(s))
  oneLoop.addOP(forecastProfit.GenForecastProfit(s))
  oneLoop.addOP(quarterProfit.GenQuarterProfit(s))
  oneLoop.addOP(quarterProfitRatio.GenQuarterProfitRatio(s))
  oneLoop.addOP(forecastQuarterProfit.GenForecastProfit(s))
  oneLoop.addOP(lastYearProfit.GenLastYearProfit(s))
  oneLoop.addOP(forecastMidGrowthRate.GenForecastMidGrowthRate(s))
  oneLoop.addOP(forecastFinalGrowthRate.GenForecastFinalGrowthRate(s))
  oneLoop.addOP(peMinMax.GenPEMinMax(s))
  oneLoop.addOP(forecastPerShareProfit.GenForecastPerShareProfit(s))
  oneLoop.addOP(forecastPE.GenForecastPE(s))
  oneLoop.addOP(valueMinMax.GenValueMinMax(s))
  oneLoop.addOP(distanceMinMax.GenDistanceMinMax(s))

  dfOut = None
  if benchmark:
    dfOut = oneLoop.verify(df, bdf)
  else:
    dfOut = oneLoop.loop(df)

  c = oneLoop.columns
  # c.extend([KEY_NAME['date'], KEY_NAME['jbmgsy'], ADJUST_NAME['zgb'], const.YJYG_KEYWORD.KEY_NAME['forecastl']])
  if saveDB:
    dfOut = oneLoop.genResult(dfOut, [KEY_NAME['jbmgsy'], ADJUST_NAME['zgb'], const.YJYG_KEYWORD.KEY_NAME['increasel']])
    #
    util.saveMongoDB(dfOut, util.genKeyDateFunc(const.MONGODB_ID), 'stock-out', 'cwsj-' + code)

  if saveFile:
    dfOut.to_excel(setting.PATH + 'out-' + code + '.xls')

  return dfOut

def runAll():
  import query.query_hs300

  stockList = setting.stock_list

  for s in stockList:
    onedf = pd.DataFrame()
    for one in s[0]:
      # if one == '603516':
      #   pass
      tmp = calcOne(one)
      tmp2 = filterOut(tmp)
      tmp3 = changeColumns(tmp2)
      if len(onedf.index) == 0:
        onedf = tmp3
      else:
        onedf = onedf.append(tmp3)

    #onedf = onedf.sort_values(by="下限距离", ascending=True)
    onedf.to_excel(s[1], index=False)

def testOne(code):
  import query.query_hs300

  stockList = [
    ([code], setting.PATH + '/out-' + code + '.xls'),
  ]

  for s in stockList:
    onedf = pd.DataFrame()
    for one in s[0]:
      # if one == '603516':
      #   pass
      tmp = calcOne(one)
      tmp2 = filterOut(tmp)
      tmp3 = changeColumns(tmp2)
      # if one == '000651':
        # tmp.to_excel('d:/stock_python/out/000651-1.xls')
        # tmp2.to_excel('d:/stock_python/out/000651-2.xls')
        # tmp3.to_excel('d:/stock_python/out/000651-3.xls')
      if len(onedf.index) == 0:
        onedf = tmp3
      else:
        onedf = onedf.append(tmp3)
    onedf.to_excel(s[1], index=False)



if __name__ == '__main__':
  testOne('601958')
  runAll()
  pass
