# -*- coding: utf-8 -*-

import time
import json

import xlwt
import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import pymongo
from pymongo import MongoClient
from pymongo import errors


FirstQuarter = '03-31'
SecondQuarter = '06-30'
ThirdQuarter = '09-30'
FourthQuarter = '12-31'


KN = {
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


client = MongoClient()
db = client['stock-adjust']
collection = db['cwsj-000725']

dbIN = client['stock']



def getYear(data):
    return data[0:4]

def getQuarter(data):
    return data[5:]


def checkDate(date):
    if len(date) != 10:
        return False

    try:
        year = date[0:4]
        month = date[5:]
        if int(year) > 2030 or int(year) < 1900:
            return False
        if month != '03-31' and \
            month != '06-30' and \
            month != '09-30' and \
            month != '12-31':
            return False

        return True

    except Exception as e:
        return False




def priorQuarter(date):
    if checkDate(date):
        if date[5:] == '12-31':
            return date[0:5] + '09-30'
        elif date[5:] == '09-30':
            return date[0:5] + '06-30'
        elif date[5:] == '06-30':
            return date[0:5] + '03-31'
        else:
            return str(int(date[0:4])-1) + '-12-31'

def getFirstQuarter(date):
    return getYear(date) + '-' + FirstQuarter



def priorXQuarter(date, x):
    date = priorQuarter(date)
    for n in range(1, x):
        if date != None:
            date = priorQuarter(date)

    return date

def priorXYear(data, x):
    year = getYear(data)
    quarter = getQuarter(data)
    newYear = str(int(year) - x)
    return newYear + '-' + quarter


def growthRate(date, data):
    yearAgo = priorXQuarter(date, 4)



def QueryTop(top, code):
    out = []
    collection = dbIN['cwsj-' + code]
    cursor = collection.find().sort(KEY_NAME['date'], pymongo.DESCENDING)
    index = 0
    for c in cursor:
        out.append(c)
        print(c)
        index += 1
        if top != -1 and index > top:
            break

    return out


def saveDB(data, key):
    collection = db['cwsj-' + key]
    if isinstance(data, list):
        for result in data:
            print(result)
            update_result = collection.update_one({'_id': result['_id']},
                                                  {'$set': result})
            if update_result.matched_count == 0:
                try:
                    if collection.insert_one(result):
                        print('Saved to Mongo')
                except errors.DuplicateKeyError as e:
                    pass
    elif isinstance(data, dict):
        for _, result in data.items():
            print(result)
            update_result = collection.update_one({'_id': result['_id']},
                                                  {'$set': result})
            if update_result.matched_count == 0:
                try:
                    if collection.insert_one(result):
                        print('Saved to Mongo')
                except errors.DuplicateKeyError as e:
                    pass


def list2Dict(key, list):
    dict = {}
    for one in list:
        dict[one[key]] = one


def genQuarterProfit(data, out):
    try:
        for i in range(0, len(data)):
            try:
                key = data[i][KEY_NAME['date']]
                profit = data[i][KEY_NAME['jbmgsy']]
                if getQuarter(key) == FirstQuarter:
                    out[key].update({KEY_NAME['date']: key, KN['QuarterProfit']: profit})
                else:
                    if i+1 < len(data):
                        out[key].update({KEY_NAME['date']: key, KN['QuarterProfit']: profit - data[i+1][KEY_NAME['jbmgsy']]})
            except TypeError as e:
                print(e)
    except KeyError as e:
        print(e)

    return out


def genQuarterProfitRatio(data, out):
    try:
        for i in range(0, len(data)):
            try:
                key = data[i][KEY_NAME['date']]
                profit = data[i][KEY_NAME['jbmgsy']]
                if getQuarter(key) == FirstQuarter:
                    out[key].update({KN['QuarterProfitRatio']: 1})
                else:
                    if getFirstQuarter(key) in out:
                        out[key].update({KN['QuarterProfitRatio']: \
                                                            out[key][KN['QuarterProfit']] \
                                                            / out[getFirstQuarter(key)][KN['QuarterProfit']]})
                    if getQuarter(key) == FourthQuarter:
                        if i+1 < len(data):
                            yearProfit = profit
                            threeQuarterProfit = data[i+1][KEY_NAME['jbmgsy']]
                            out[key].update({KN['ThreeQuarterProfitRatio']: (yearProfit-threeQuarterProfit)/threeQuarterProfit})
                            if i+2 < len(data):
                                yearProfit = profit
                                halfYearQuarterProfit = data[i+2][KEY_NAME['jbmgsy']]
                                out[key].update(
                                    {KN['HalfYearProfitRatio']: (yearProfit - halfYearQuarterProfit) / halfYearQuarterProfit})
            except TypeError as e:
                print(e)
    except KeyError as e:
        print(e)

    return out


def genQuarterForecastGrowthRate(data, out):
    try:
        for i in range(0, len(data)):
            try:
                key = data[i][KEY_NAME['date']]
                profit = data[i][KEY_NAME['jbmgsy']]
                if getQuarter(key) == FirstQuarter:
                    if priorXYear(key, 1) in out:
                        last4thQuarter = out[priorXQuarter(key, 1)]
                        last3thQuarter = out[priorXQuarter(key, 2)]
                        last2thQuarter = out[priorXQuarter(key, 3)]
                        forecast = ((profit + profit*last4thQuarter[KN['QuarterProfitRatio']] + \
                                     profit * last3thQuarter[KN['QuarterProfitRatio']] + \
                                     profit * last2thQuarter[KN['QuarterProfitRatio']]) / data[i+1][KEY_NAME['jbmgsy']]) - 1

                        out[key].update({KN['ForecastGrowthRate']: forecast})
                elif getQuarter(key) == SecondQuarter:
                    if priorXQuarter(key, 2) in out and i+2 < len(data):
                        last4thQuarter = out[priorXQuarter(key, 2)]
                        forecast = ((profit + profit*last4thQuarter[KN['HalfYearProfitRatio']]) / data[i+2][KEY_NAME['jbmgsy']]) - 1
                        out[key].update({KN['ForecastGrowthRate']: forecast})
                elif getQuarter(key) == ThirdQuarter:
                    if priorXQuarter(key, 3) in out and i+3 < len(data):
                        last4thQuarter = out[priorXQuarter(key, 3)]
                        forecast = ((profit + profit * last4thQuarter[KN['ThreeQuarterProfitRatio']]) / data[i + 3][
                            KEY_NAME['jbmgsy']]) - 1

                        out[key].update({KN['ForecastGrowthRate']: forecast})
                else:
                    if priorXQuarter(key, 4) in out:
                        try:
                            forecast = (profit / data[i + 4][KEY_NAME['jbmgsy']]) - 1
                            out[key].update({KN['ForecastGrowthRate']: forecast})
                        except IndexError as e:
                            print(e)
            except TypeError as e:
                print(e)
    except KeyError as e:
        print(e)

    return out

def prepareResult(data):
    out = {}
    for one in data:
        out[one[KEY_NAME['date']]] = {'_id': one[KEY_NAME['date']]}

    return out


if __name__ == '__main__':
    index = 0
    for one in STOCK_LIST:
        re = QueryTop(-1, one)
        out = prepareResult(re)
        out = genQuarterProfit(re, out)
        out = genQuarterProfitRatio(re, out)
        out = genQuarterForecastGrowthRate(re, out)
        saveDB(out, one)

        # index += 1
        # if index > 0:
        #     break


    pass