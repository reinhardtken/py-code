# -*- coding: utf-8 -*-

# sys
import datetime
import re

# thirdpart
import pandas as pd
import pymongo
from pymongo import MongoClient
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, DateFormatter

#this project
import query
import util
import const


def drawUnitPriceTrend(df, district):
  fig = plt.figure(figsize=(12, 6))
  ax = fig.add_subplot(1, 1, 1)
  ax.set_title(district)
  # https://www.zhihu.com/question/25404709
  mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
  mpl.rcParams['axes.unicode_minus'] = False
  grouped = df.groupby('houseSize')
  for k, v in grouped:
    x = v['month'].values.tolist()
    y = v['price'].values.tolist()
    plt.plot(x, y, label=k)

    # plt.text(x[0], y[0], k, horizontalalignment='right', verticalalignment='bottom')
  # 设置X轴的时间间隔，MinuteLocator、HourLocator、DayLocator、WeekdayLocator、MonthLocator、YearLocator
  # plt.gca().xaxis.set_major_locator(DayLocator(interval=90))
  # 设置X轴的时间显示格式
  # plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m'))
  # ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
  # 自动旋转X轴的刻度，适应坐标轴
  plt.gcf().autofmt_xdate()
  plt.grid(True)
  plt.legend(bbox_to_anchor=(1.0, 0.9))
  plt.show()
  plt.xlabel(district)



def drawDealNumberTrend(df, district):
  fig = plt.figure(figsize=(12, 6))
  ax = fig.add_subplot(1, 1, 1)
  ax.set_title(district)
  # https://www.zhihu.com/question/25404709
  mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
  mpl.rcParams['axes.unicode_minus'] = False

  grouped = df.groupby('houseSize')
  for k, v in grouped:
    x = v['month'].values.tolist()
    y = v['number'].values.tolist()
    plt.plot(x, y, label=k)


    # plt.text(x[0], y[0], k, horizontalalignment='right', verticalalignment='bottom')
  # 设置X轴的时间间隔，MinuteLocator、HourLocator、DayLocator、WeekdayLocator、MonthLocator、YearLocator
  # plt.gca().xaxis.set_major_locator(DayLocator(interval=90))
  # 设置X轴的时间显示格式
  # plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m'))
  # ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
  # 自动旋转X轴的刻度，适应坐标轴
  plt.gcf().autofmt_xdate()
  plt.grid(True)
  plt.legend(bbox_to_anchor=(1.0, 0.9))
  plt.show()
  plt.xlabel(district)


def drawTrend(df, district, by, xKey, yKey):
  fig = plt.figure(figsize=(12, 6))
  ax = fig.add_subplot(1, 1, 1)
  ax.set_title(district)
  # https://www.zhihu.com/question/25404709
  mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
  mpl.rcParams['axes.unicode_minus'] = False

  grouped = df.groupby(by)
  for k, v in grouped:
    x = v[xKey].values.tolist()
    y = v[yKey].values.tolist()
    plt.plot(x, y, label=k)


    # plt.text(x[0], y[0], k, horizontalalignment='right', verticalalignment='bottom')
  # 设置X轴的时间间隔，MinuteLocator、HourLocator、DayLocator、WeekdayLocator、MonthLocator、YearLocator
  # plt.gca().xaxis.set_major_locator(DayLocator(interval=90))
  # 设置X轴的时间显示格式
  # plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m'))
  # ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
  # 自动旋转X轴的刻度，适应坐标轴
  plt.gcf().autofmt_xdate()
  plt.grid(True)
  plt.legend(bbox_to_anchor=(1.0, 0.9))
  plt.show()
  plt.xlabel(district)



def calcSize(x):
  size = int(x)
  if size < 40:
    return '<40平'
  elif size >= 40 and size < 60:
    return '40-60平'
  elif size >= 60 and size < 80:
    return '60-80平'
  elif size >= 80 and size < 100:
    return '80-100平'
  elif size >= 100 and size < 120:
    return '100-120平'
  elif size >= 120 and size < 140:
    return '120-140平'
  else:
    return '>=140平'

def toYearMonth(x):
  return x.strftime('%Y-%m')
  # return x.replace(day=0, hour=0, minute=0, second=0, microsecond=0)


def unitPriceTrend(df):
  out = []

  df['houseSize'] = df['square'].map(calcSize)
  g = df.groupby('houseSize')
  for k, v in g:
    # g2 = v.groupby(lambda x : x['dealDate'].month)
    # g2 = v.groupby('dealDate').apply(func)
    v['month'] = v['dealDate'].map(toYearMonth)
    g2 = v.groupby('month')
    for k2, v2 in g2:
      # print(k2)
      # print(v2)
      price = v2['unitPrice'].mean()
      out.append({'month': k2, 'price': price, 'houseSize': k})

  outDf = pd.DataFrame(out)
  # outDf.set_index('month', inplace=True)
  # outDf.plot(x='month', y='price')
  # plt.show()
  drawUnitPriceTrend(outDf, district)


def dealNumberTrend(df):
  out = []
  df['houseSize'] = df['square'].map(calcSize)
  g = df.groupby('houseSize')
  for k, v in g:
    # g2 = v.groupby(lambda x : x['dealDate'].month)
    # g2 = v.groupby('dealDate').apply(func)
    v['month'] = v['dealDate'].map(toYearMonth)
    g2 = v.groupby('month')
    for k2, v2 in g2:
      # print(k2)
      # print(v2)
      number = len(v2)
      out.append({'month': k2, 'number': number, 'houseSize': k})

  outDf = pd.DataFrame(out)
  # outDf.set_index('month', inplace=True)
  # outDf.plot(x='month', y='price')
  # plt.show()
  drawDealNumberTrend(outDf, district)


def dealCycleTrend(df):
  out = []

  df['houseSize'] = df['square'].map(calcSize)
  g = df.groupby('houseSize')
  for k, v in g:
    v['month'] = v['dealDate'].map(toYearMonth)
    g2 = v.groupby('month')
    for k2, v2 in g2:
      # print(k2)
      # print(v2)
      dealCycle = v2['dealCycle'].mean()
      out.append({'month': k2, 'dealCycle': dealCycle, 'houseSize': k})

  outDf = pd.DataFrame(out)
  # outDf.set_index('month', inplace=True)
  # outDf.plot(x='month', y='price')
  # plt.show()
  drawTrend(outDf, district, 'houseSize', 'month', 'dealCycle')


def diffPriceTrend(df):
  out = []

  df['houseSize'] = df['square'].map(calcSize)
  g = df.groupby('houseSize')
  for k, v in g:
    v['month'] = v['dealDate'].map(toYearMonth)
    g2 = v.groupby('month')
    for k2, v2 in g2:
      # print(k2)
      # print(v2)
      diffPricePercent = v2['diffPricePercent'].mean()
      out.append({'month': k2, 'diffPricePercent': diffPricePercent, 'houseSize': k})

  outDf = pd.DataFrame(out)
  drawTrend(outDf, district, 'houseSize', 'month', 'diffPricePercent')



def analyzeCityPriceTrendDigest(city, src, week):
  try:
    df = query.queryCityPriceTrend(city, src, week)
    if df is None or len(df) == 0:
      return

    upGroup = df.loc[lambda df: df.trend == 1, :]
    downGroup = df.loc[lambda df: df.trend == -1, :]
    upMean = upGroup['diffPercent'].mean()
    downMean = downGroup['diffPercent'].mean()

    client = MongoClient()
    db = client['house-trend']
    collection = db['priceTrend']
    data = {
      '_id': city + '_' + src + '_' + str(week),
      'city': city,
      'src': src,
      'week': week,
      'up': len(upGroup),
      'down': len(downGroup),
      'upDiff': upMean,
      'downDiff': downMean,
    }

    try:
      update_result = collection.insert_one(data)

    except pymongo.errors.DuplicateKeyError as e:
      pass
      # print('DuplicateKeyError to Mongo!!!: %s : %s : %s' % (self.dbName, self.collectionName, data['_id']))
    except Exception as e:
      print(e)

  except Exception as e:
    print(e)


def analyzeCityAvgPriceDigest(city, src):
  df2 = query.querySecondHandData(city, src)
  if df2 is None or len(df2) == 0:
    return

  df = df2.loc[lambda df2: np.isnan(df2.square) == False, :]

  df.loc[:, 'houseSize'] = df['square'].map(calcSize)
  g = df.groupby('houseSize')
  out = []
  for k, v in g:
    # g2 = v.groupby(lambda x : x['dealDate'].month)
    # g2 = v.groupby('dealDate').apply(func)
    unitPrice = v['unitPrice'].mean()
    week = util.getWeekofYear()
    one = {
      '_id': city + '_' + src + '_' + str(week) + '_' + k,
      'city': city,
      'src': src,
      'houseSize': k,
      'unitPrice': unitPrice,
      'number': len(v),
      'weekofYear': week
    }
    out.append(one)

  client = MongoClient()
  db = client['house-trend']
  collection = db['unitPriceAvg']


  try:
    for one in out:
      update_result = collection.insert_one(one)

  except pymongo.errors.DuplicateKeyError as e:
    pass
  except Exception as e:
    print(e)




def analyzeDistrictAvgPriceDigest(city, src):
  df2 = query.querySecondHandData(city, src)
  if df2 is None or len(df2) == 0:
    return

  df = df2.loc[lambda df2: np.isnan(df2.square) == False, :]

  df.loc[:, 'houseSize'] = df['square'].map(calcSize)
  g = df.groupby('district')
  out = []
  for k, v in g:
    g2 = v.groupby('houseSize')
    for k2, v2 in g2:
      week = util.getWeekofYear()
      unitPrice = v2['unitPrice'].mean()
      one = {
        '_id': city + '_' + k + '_' + src + '_' + str(week) + '_' + k2,
        'city': city,
        'district': k,
        'src': src,
        'houseSize': k2,
        'unitPrice': unitPrice,
        'number': len(v2),
        'weekofYear': week,
      }
      out.append(one)

  client = MongoClient()
  db = client['house-trend']
  collection = db['districtUnitPriceAvg']


  try:
    for one in out:
      update_result = collection.insert_one(one)

  except pymongo.errors.DuplicateKeyError as e:
    pass
  except Exception as e:
    print(e)



# this project
if __name__ == '__main__':
  # srcs = const.SRCS
  srcs = ['wiwj']
  citys = const.CITYS
  for src in srcs:
    for city in citys:
      analyzeCityPriceTrendDigest(city, src, 201838)
  #     #analyzeCityAvgPriceDigest(city, src)
  #     #analyzeDistrictAvgPriceDigest(city, src)
  #     pass




  # # city = 'shanghai'
  # # districts = ['浦东', '静安', '黄浦', '徐汇']
  #city = 'beijing'
  #districts = ['海淀', '朝阳', '东城', '西城']
  # # city = 'changsha'
  # # districts = ['开福', '雨花', '芙蓉', '岳麓', '天心']
  # # city = 'shenzhen'
  # # districts = ['南山区', '福田区', '宝安区', '罗湖区']
  city = 'langfang'
  districts = ['廊坊', ]
  #
  #
  now = datetime.datetime.now()
  thisYear = now.replace(year=2015, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
  august = now.replace(month=8, day=1, hour=0, minute=0, second=0, microsecond=0)
  #
  for district in districts:
    df = query.queryTurnOverData(city, district, (thisYear, august))
    unitPriceTrend(df)
    #dealNumberTrend(df)
  #   # dealCycleTrend(df)
  #   # diffPriceTrend(df)
  # pass