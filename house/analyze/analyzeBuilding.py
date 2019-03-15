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



def drawTrend(df, district, by, xKey, yKey):
  fig = plt.figure(figsize=(12, 6))
  ax = fig.add_subplot(1, 1, 1)
  ax.set_title(district)
  # https://www.zhihu.com/question/25404709
  mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
  mpl.rcParams['axes.unicode_minus'] = False

  if len(by):
    grouped = df.groupby(by)
    for k, v in grouped:
      # x = v[xKey].values.tolist()
      x = v[xKey].tolist()
      y = v[yKey].values.tolist()
      plt.plot(x, y, label=k)
  else:
    x = df[xKey].tolist()
    y = df[yKey].values.tolist()
    plt.plot(x, y, )

    # plt.text(x[0], y[0], k, horizontalalignment='right', verticalalignment='bottom')
  # 设置X轴的时间间隔，MinuteLocator、HourLocator、DayLocator、WeekdayLocator、MonthLocator、YearLocator
  # plt.gca().xaxis.set_major_locator(DayLocator(interval=90))
  # 设置X轴的时间显示格式
  # plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m'))
  # ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
  # 自动旋转X轴的刻度，适应坐标轴
  ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
  plt.gcf().autofmt_xdate()
  plt.grid(True)
  plt.legend(bbox_to_anchor=(1.0, 0.9))
  plt.show()
  plt.xlabel(district)



def calcSize(x):
  if np.isnan(x):
    size = 35
  else:
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
  #return x.strftime('%Y-%m')
  return x.replace(day=15, hour=0, minute=0, second=0, microsecond=0)


def unitPriceTrend(df, building):
  out = []

  # df.eval('unitPrice = bidPrice / square')
  df['unitPrice'] = df['bidPrice'] / df['square']
  df.loc[:, 'month'] = df['dealDate'].map(toYearMonth)
  # v.sort_values("month", inplace=True)
  g2 = df.groupby('month')
  for k2, v2 in g2:

    price = v2['unitPrice'].mean()
    out.append({'month': k2, 'price': price, })


  outDf = pd.DataFrame(out)
  drawTrend(outDf, building, '', 'month', 'price')





# this project
if __name__ == '__main__':


  now = datetime.datetime.now()
  thisYear = now.replace(year=2015, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
  august = now.replace(month=12, day=1, hour=0, minute=0, second=0, microsecond=0)

  buildings = [
    u'佳运园二期',
    u'溪城家园',
    u'佳运园一期',
    u'北方明珠',
    u'嘉诚花园二期',
    u'嘉诚花园一期',

  ]
  # building =
  for building in buildings:
    df = query.queryBuildTurnOverData(building, (thisYear, august))
    unitPriceTrend(df, building)