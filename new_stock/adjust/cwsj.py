# -*- coding: utf-8 -*-

#sys
import json

#thirdpart
import pandas as pd

#this project
if __name__ == '__main__':
    import sys
    sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils
import const


from query import query_adjust_cwsj
from query import query_cwsj

KN = const.CWSJ_KEYWORD.ADJUST_NAME
KEY_NAME = const.CWSJ_KEYWORD.KEY_NAME


def genQuarterProfit(baseData, adjustData):
    for date, row in baseData.iterrows():
        profit = row[KEY_NAME['jbmgsy']]
        if util.isSameQuarter(date, util.FirstQuarter):
            # adjustData.ix[date][KN['QuarterProfit']] = profit
            adjustData.loc[date, KN['QuarterProfit']] = profit
        else:
            priorDate = util.priorQuarter(date)
            try:
                priorData = baseData.loc[priorDate]
                try:
                    adjustData.loc[date, KN['QuarterProfit']] = profit - priorData.loc[KEY_NAME['jbmgsy']]
                except TypeError as e:
                    print(e)
            except KeyError as e:
                print(e)


    return adjustData


def genQuarterProfitRatio(baseData, adjustData):
    for date, row in baseData.iterrows():
        if util.isSameQuarter(date, util.FirstQuarter):
            adjustData.loc[date, KN['QuarterProfitRatio']] = 1
        else:
            firstQuarter = util.getFirstQuarter(date)
            try:
                firstData = adjustData.loc[firstQuarter]
                try:
                    adjustData.loc[date, KN['QuarterProfitRatio']] = adjustData.loc[date, KN['QuarterProfit']] / firstData.loc[KN['QuarterProfit']]
                    if util.isSameQuarter(date, util.FourthQuarter):
                        priorDate = util.priorQuarter(date)
                        priorData = baseData.loc[priorDate]
                        yearProfit = row[KEY_NAME['jbmgsy']]
                        threeQuarterProfit = priorData.loc[KEY_NAME['jbmgsy']]
                        adjustData.loc[date, KN['ThreeQuarterProfitRatio']] = (yearProfit - threeQuarterProfit) / threeQuarterProfit

                        prior2Date = util.priorXQuarter(date, 2)
                        prior2Data = baseData.loc[prior2Date]
                        halfYearQuarterProfit = prior2Data.loc[KEY_NAME['jbmgsy']]
                        adjustData.loc[date, KN['HalfYearProfitRatio']] = (yearProfit - halfYearQuarterProfit) / halfYearQuarterProfit

                except TypeError as e:
                    print(e)
            except KeyError as e:
                print(e)

    return adjustData



def genQuarterForecastGrowthRate(baseData, adjustData):
    for date, row in baseData.iterrows():
        profit = row[KEY_NAME['jbmgsy']]
        try:
            if util.isSameQuarter(date, util.FirstQuarter):
                priorDateBegin = util.priorQuarter(date)
                priorDateEnd = util.priorXQuarter(date, 3)
                priorData = adjustData.loc[priorDateBegin:priorDateEnd]
                last4thQuarter = priorData.loc[priorDateBegin, KN['QuarterProfitRatio']]
                last3thQuarter = priorData.loc[util.priorXQuarter(date, 2), KN['QuarterProfitRatio']]
                last2thQuarter = priorData.loc[priorDateEnd, KN['QuarterProfitRatio']]
                forecast = ((profit + profit * last4thQuarter + \
                             profit * last3thQuarter + \
                             profit * last2thQuarter) / baseData.loc[util.priorQuarter(date), KEY_NAME['jbmgsy']]) - 1

                adjustData.loc[date, KN['ForecastGrowthRate']] = forecast

            elif util.isSameQuarter(date, util.SecondQuarter):
                last4thQuarter = adjustData.loc[util.priorXQuarter(date, 2)]
                forecast = ((profit + profit * last4thQuarter.loc[KN['HalfYearProfitRatio']]) \
                   / baseData.loc[util.priorXQuarter(date, 2), KEY_NAME['jbmgsy']]) - 1
                adjustData.loc[date, KN['ForecastGrowthRate']] = forecast

            elif util.isSameQuarter(date, util.ThirdQuarter):
                last4thQuarter = adjustData.loc[util.priorXQuarter(date, 3)]
                forecast = ((profit + profit * last4thQuarter.loc[KN['ThreeQuarterProfitRatio']]) \
                            / baseData.loc[util.priorXQuarter(date, 3), KEY_NAME['jbmgsy']]) - 1

                adjustData.loc[date, KN['ForecastGrowthRate']] = forecast

            else:
                forecast = (profit / baseData.loc[util.priorXQuarter(date, 4), KEY_NAME['jbmgsy']]) - 1
                adjustData.loc[date, KN['ForecastGrowthRate']] = forecast
        except KeyError as e:
            print(e)

    return adjustData


def genPerShareProfitForecast(baseData, adjustData):
    for date, row in adjustData.iterrows():
        try:
            if util.isSameQuarter(date, util.FirstQuarter):
                ratio1 = adjustData.loc[util.priorQuarter(date), KN['QuarterProfitRatio']]
                ratio2 = adjustData.loc[util.priorXQuarter(date, 2), KN['QuarterProfitRatio']]
                ratio3 = adjustData.loc[util.priorXQuarter(date, 3), KN['QuarterProfitRatio']]
                adjustData.loc[date, KN['PerShareProfitForecast']] = row.loc[KN['QuarterProfit']] * \
                                                        (1+ratio1+ratio2+ratio3)
                # adjustData.loc[date, KN['QuarterProfitRatio']] = 1
            elif util.isSameQuarter(date, util.SecondQuarter):
                ratio = adjustData.loc[util.priorXQuarter(date, 2), KN['HalfYearProfitRatio']]
                adjustData.loc[date, KN['PerShareProfitForecast']] = baseData.loc[date, KEY_NAME['jbmgsy']] * (1 + ratio)
            elif util.isSameQuarter(date, util.ThirdQuarter):
                ratio = adjustData.loc[util.priorXQuarter(date, 3), KN['ThreeQuarterProfitRatio']]
                adjustData.loc[date, KN['PerShareProfitForecast']] = baseData.loc[date, KEY_NAME['jbmgsy']] * (1 + ratio)
            else:
                adjustData.loc[date, KN['PerShareProfitForecast']] = baseData.loc[date, KEY_NAME['jbmgsy']]

        except KeyError as e:
            print(e)

    return adjustData

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

    adjustData = genQuarterProfit(baseData, adjustData)
    adjustData = genQuarterProfitRatio(baseData, adjustData)
    adjustData = genQuarterForecastGrowthRate(baseData, adjustData)
    adjustData = genPerShareProfitForecast(baseData, adjustData)
    util.saveMongoDB(adjustData, util.genKeyDateFunc(KN['date']), 'stock-adjust', 'cwsj-' + code)



if __name__ == '__main__':
    test('000725')


    pass