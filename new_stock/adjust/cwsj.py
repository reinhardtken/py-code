# -*- coding: utf-8 -*-

import datetime
import json

import xlwt
import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import pymongo
from pymongo import MongoClient
from pymongo import errors
import pandas as pd

from query import query_adjust_cwsj
from query import query_cwsj
import util



KN = {
'_id': '_id',
"date": "季度",
'QuarterProfit': '当季每股收益',
'QuarterProfitRatio': '较一季度比例',
'HalfYearProfitRatio': '较上半年比例',
'ThreeQuarterProfitRatio': '较前三季度比例',
'ForecastGrowthRate': '预测增长率',
}

KEY_NAME = {
    "date": "季度",
"jbmgsy": "基本每股收益(元)",
"kfmgsy": "扣非每股收益(元)",
"xsmgsy": "稀释每股收益(元)",
"mgjzc": "每股净资产(元)",
"mggjj": "每股公积金(元)",
"mgwfply": "每股未分配利润(元)",
"mgjyxjl": "每股经营现金流(元)",
"yyzsr": "营业总收入(元)",
"mlr": "毛利润(元)",
"gsjlr": "归属净利润(元)",
"kfjlr": "扣非净利润(元)",
"yyzsrtbzz": "营业总收入同比增长(%)",
"gsjlrtbzz": "归属净利润同比增长(%)",
"kfjlrtbzz": "扣非净利润同比增长(%)",
"yyzsrgdhbzz": "营业总收入滚动环比增长(%)",
"gsjlrgdhbzz": "归属净利润滚动环比增长(%)",
"kfjlrgdhbzz": "扣非净利润滚动环比增长(%)",
"jqjzcsyl": "加权净资产收益率(%)",
"tbjzcsyl": "摊薄净资产收益率(%)",
"tbzzcsyl": "摊薄总资产收益率(%)",
"mll": "毛利率(%)",
"jll": "净利率(%)",
"sjsl": "实际税率(%)",
"yskyysr": "预收款/营业收入",
"xsxjlyysr": "销售现金流/营业收入",
"jyxjlyysr": "经营现金流/营业收入",
"zzczzy": "总资产周转率(次)",
"yszkzzts": "应收账款周转天数(天)",
"chzzts": "存货周转天数(天)",
"zcfzl": "资产负债率(%)",
"ldzczfz": "流动负债/总负债(%)",
"ldbl": "流动比率",
"sdbl": "速动比率"}


STOCK_LIST = {
'000725',
"000651",
"002508",
"600566",
"600487",
"300298",
"300642",
"603595",
"603156",
"603868",
"002517",
"603387",
"600690",
"300628",
"002626",
"002294",
"002372",
"002415",
"603516",
"002901",
"000848",
"002032",
"603833",
"603160",
"002304",
"600519",
"300741",
"603288",
}


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

def prepareResult(data):
    df = pd.DataFrame(columns=KN.values())
    df['_id'] = data['_id']
    df[KN['date']] = data.index
    df.set_index(KN['date'], inplace=True)
    return df


def test():
    CODE = '000725'
    baseData = query_cwsj.QueryTop(-1, CODE)
    adjustData = query_adjust_cwsj.QueryTop(-1, CODE)
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
    util.saveMongoDB(adjustData, KN['date'], 'stock-adjust', 'cwsj-' + CODE)



if __name__ == '__main__':
    # index = 0
    # for one in STOCK_LIST:
    #     re = QueryTop(-1, one)
    #     out = prepareResult(re)
    #     out = genQuarterProfit(re, out)
    #     out = genQuarterProfitRatio(re, out)
    #     out = genQuarterForecastGrowthRate(re, out)
    #

        # index += 1
        # if index > 0:
        #     break


    pass