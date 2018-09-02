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
  elif size >= 41 and size < 60:
    return '40-60平'
  elif size >= 61 and size < 80:
    return '60-80平'
  elif size >= 81 and size < 100:
    return '80-100平'
  else:
    return '>100平'

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

# this project
if __name__ == '__main__':
  # city = 'shanghai'
  # districts = ['浦东', '静安', '黄浦', '徐汇']
  city = 'beijing'
  districts = ['海淀', '朝阳', '东城', '西城']
  # city = 'changsha'
  # districts = ['开福', '雨花', '芙蓉', '岳麓', '天心']


  now = datetime.datetime.now()
  thisYear = now.replace(year=2018, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
  august = now.replace(month=8, day=1, hour=0, minute=0, second=0, microsecond=0)

  for district in districts:
    df = query.queryTurnOverData(city, district, (thisYear, august))
    unitPriceTrend(df)
    # dealNumberTrend(df)
    # dealCycleTrend(df)
    # diffPriceTrend(df)
  pass