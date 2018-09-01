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


def calcSize(x):
  size = int(x/10)
  if size <= 3:
    return 3
  elif size >= 10:
    return 10
  else:
    return size

def toYearMonth(x):
  return x.strftime('%Y-%m')
  # return x.replace(day=0, hour=0, minute=0, second=0, microsecond=0)


def unitPriceTrend(district):
  out = []
  df = query.queryTurnOverData('beijing', district)
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


def dealNumberTrend(district):
  out = []
  df = query.queryTurnOverData('beijing', district)
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

# this project
if __name__ == '__main__':
  districts = ['海淀', '朝阳', '东城', '西城']
  for district in districts:
    unitPriceTrend(district)
    # dealNumberTrend(district)
  pass