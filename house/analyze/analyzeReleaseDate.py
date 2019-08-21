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


def String2Number(s):
  out = np.nan
  try:
    out = float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])
  except Exception as e:
    pass

  return out


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
  # ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
  plt.gcf().autofmt_xdate()
  plt.grid(True)
  plt.legend(bbox_to_anchor=(1.0, 0.9))
  plt.show()
  plt.xlabel(district)



def calcDay(x):

  number = String2Number(x)
  if '天' in x:
    pass
  elif '月' in x:
    number *= 30
  elif '一年' in x:
    number = 366


  if number < 31:
    return '1个月内'
  elif number >= 31 and number < 60:
    return '2个月内'
  elif number >= 61 and number < 90:
    return '3个月内'
  elif number >= 91 and number < 180:
    return '半年内'
  elif number >= 181 and number < 270:
    return '3个季度内'
  elif number >= 271 and number < 365:
    return '1年内'
  else:
    return '1年以上'

def toYearMonth(x):
  #return x.strftime('%Y-%m')
  return x.replace(day=15, hour=0, minute=0, second=0, microsecond=0)


def releaseDate(df, city):
  out = []

  df['releaseDay'] = df['release'].map(calcDay)

  # v.sort_values("month", inplace=True)
  g2 = df.groupby('releaseDay')
  for k2, v2 in g2:

    number = len(v2)
    out.append({'releaseDay': k2, 'number': number, })


  outDf = pd.DataFrame(out)
  drawTrend(outDf, city, '', 'releaseDay', 'number')





# this project
if __name__ == '__main__':


  now = datetime.datetime.now()
  thisYear = now.replace(year=2015, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
  august = now.replace(month=12, day=1, hour=0, minute=0, second=0, microsecond=0)

  citys = [
    'beijing'

  ]
  # building =
  for city in citys:
    df = query.queryReleaseData(city, 'lj')
    releaseDate(df, city)