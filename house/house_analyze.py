#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import urlparse
import bs4
import xlwt
import xlrd
import time
import datetime
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.dates import DayLocator, DateFormatter
import pandas as pd
import datetime

######################################################################
def StringTime2TimeWithFormat(data, format):
  return datetime.datetime.strptime(data, format)


def StringTime2Time1(data):
  #2013-07-01
  return StringTime2TimeWithFormat(data, '%Y-%m-%d')
######################################################################
IN_DIR = r'C:\workspace\house\cs'
OUT_DIR = r'C:\workspace\house\cs\analyze'


# Traversal(codeDir, self.ProcessOneFile, ".java")
def Traversal(base_dir, action, ext):
  if base_dir == None or action == None or ext == None:
    return

  exts = ext.split("|")

  def EndsWith(name):
    for v in exts:
      if name.endswith(v):
        return True
    return False

  for parent, dirnames, filenames in os.walk(base_dir):
    for filename in filenames:
      # absolute_filename = os.path.join(parent,filename)
      if ext != None and EndsWith(filename):
        action(parent, filename)




class Digest:
  KEY_DATE = u'采样日期'
  KEY_TOTAL = u'总套数'
  KEY_TOTAL_PRICE = u'平均总价'
  KEY_AVR_SQUARE = u'平均面积'
  KEY_AVR_PRICE = u'平均单价'
  KEY_AVR_LOOK = u'平均带看'
  KEY_AVR_ATTENTION = u'平均关注'
  KEY_AVR_RELEASE = u'平均发布'
  def __init__(self):
    self.name = None
    self.date = None
    self.total = None
    self.total_price = None
    self.avg_square = None
    self.avg_price = None
    self.avg_look = None
    self.avg_attention = None
    self.avg_release = None
    
    
  def __cmp__(self, other):
    if self.__eq__(other):
      return 0
    elif self.__lt__(other):
      return -1
    elif self.__gt__(other):
      return 1

  def __lt__(self, other):
    d1 = StringTime2Time1(self.date)
    d2 = StringTime2Time1(other.date)
    return d1 < d2

  def __eq__(self, other):
    d1 = StringTime2Time1(self.date)
    d2 = StringTime2Time1(other.date)
    return d1 == d2

  def __gt__(self, other):
    d1 = StringTime2Time1(self.date)
    d2 = StringTime2Time1(other.date)
    return d1 > d2


  def AddValue(self, k, v):
    if k == Digest.KEY_DATE:
      self.date = v
    elif k == Digest.KEY_TOTAL:
      self.total = v
    elif k == Digest.KEY_TOTAL_PRICE:
      self.total_price = v
    elif k == Digest.KEY_AVR_SQUARE:
      self.avg_square = v
    elif k == Digest.KEY_AVR_PRICE:
      self.avg_price = v
    elif k == Digest.KEY_AVR_LOOK:
      self.avg_look = v
    elif k == Digest.KEY_AVR_ATTENTION:
      self.avg_attention = v
    elif k == Digest.KEY_AVR_RELEASE:
      self.avg_release = v

class Analyze:
  KEY_MAP = {
  u'采样日期':'KEY_DATE',
  u'总套数':'KEY_TOTAL',
  u'平均总价':'KEY_TOTAL_PRICE',
  u'平均面积':'KEY_AVR_SQUARE',
  u'平均单价':'KEY_AVR_PRICE',
  u'平均带看':'KEY_AVR_LOOK',
  u'平均关注':'KEY_AVR_ATTENTION',
  u'平均发布':'KEY_AVR_RELEASE'}

  def __init__(self, inDir, outDir):
    self.inDir = inDir
    self.outDir = outDir

    #每个excel文件，按名字一个key，value是按时间分布的文件集合
    self.districtMap = {}


  def CollectFile(self, parent, filename):
    if parent.endswith('analyze'):
      return
    print(parent + '\\' + filename)
    name = filename.split('.')[0]
    if self.districtMap.has_key(name):
      self.districtMap[name].append(parent + '\\' + filename)
    else:
      temp = []
      temp.append(parent + '\\' + filename)
      self.districtMap[name] = temp

  def Traversal(self):
    Traversal(self.inDir, self.CollectFile, 'xls')

  def Analyze(self):
    drawInfo = []
    for k,v in self.districtMap.iteritems():
      drawInfo.append(self.AnalyzeOne(k, v))

    #draw
    self.Draw(drawInfo)

  def Draw(self, info):
    plt.figure(figsize=(12, 6))
    #https://www.zhihu.com/question/25404709
    mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
    mpl.rcParams['axes.unicode_minus'] = False
    for i in info:
      x = [StringTime2Time1(one.date) for one in i[1]]
      y = [one.avg_price for one in i[1]]
      plt.plot(x, y, label=i[0])

      plt.text(StringTime2Time1(i[1][0].date), i[1][0].avg_price, i[0],
              horizontalalignment='right',
              verticalalignment='bottom')
    # 设置X轴的时间间隔，MinuteLocator、HourLocator、DayLocator、WeekdayLocator、MonthLocator、YearLocator
    #plt.gca().xaxis.set_major_locator(DayLocator(interval=90))
    # 设置X轴的时间显示格式
    plt.gca().xaxis.set_major_formatter(DateFormatter('%y/%m/%d'))
    # 自动旋转X轴的刻度，适应坐标轴
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.show()



  def ReadOneSheet(self, subDistrictList, name, workbook):

    sheet = workbook.sheet_by_name(name)
    '''
    sheet.nrows　　　　sheet的行数
    sheet.row_values(index)　　　　返回某一行的值列表
　　sheet.row(index)　　　　返回一个row对象，可以通过row[index]来获取这行里的单元格cell对象'''
    nrows = sheet.nrows
    # 如果超过20行，从倒数十行开始提取摘要，否则从头开始提取
    digest = Digest()
    digest.name = name
    start = None
    if nrows > 20:
      start = nrows - 10
    else:
      start = 1
    for index in xrange(start, nrows):
      print(nrows)
      print(index)
      # print(district)
      print(name)
      value = sheet.row_values(index)
      row = sheet.row(index)
      print(row[0])
      print(Analyze.KEY_MAP)
      # tmp = u'采样日期'
      key = row[0].value.strip()
      if Analyze.KEY_MAP.has_key(key):
        digest.AddValue(key, row[1].value)

    subDistrictList.append(digest)



  def AnalyzeOne(self, district, v):
    #一个子区，每周平均数据汇总
    oneSubDistrictMap = {}
    #这两个记录整体信息
    oneSubDistrictFirstName = None
    oneSubDistrictFirstList = []
    writebook = xlwt.Workbook()
    for one in v:
      '''
      workbook = xlrd.open_workbook('文件路径')
      workbook.sheet_names()    #返回所有sheet的列表
      workbook.sheet_by_index(...)    #通过index来获得一个sheet对象，index从0开始算起
      workbook.sheet_by_name(...)    #根据sheet名获得相应的那个sheet对象'''
      workbook = xlrd.open_workbook(one)
      names = workbook.sheet_names()
      oneSubDistrictFirstName = names[0]
      self.ReadOneSheet(oneSubDistrictFirstList, oneSubDistrictFirstName, workbook)

      #读sheet
      for index in xrange(1, len(names)):
        if oneSubDistrictMap.has_key(names[index]):
          pass
        else:
          oneSubDistrictMap[names[index]] = []
        self.ReadOneSheet(oneSubDistrictMap[names[index]], names[index], workbook)

    #汇总数据需要安时间排序，现在在文件夹里面的，是按字符串排序，并非严格的时间序列
    oneSubDistrictFirstList.sort()
    # 写excel
    for k, v in oneSubDistrictMap.iteritems():
      v.sort()
    
    self.WriteSheet(writebook, oneSubDistrictFirstName, oneSubDistrictFirstList)
    #写excel
    for k, v in oneSubDistrictMap.iteritems():
      self.WriteSheet(writebook, k, v)

    writebook.save(self.outDir + '/' + district + '.xls')

    return (oneSubDistrictFirstName, oneSubDistrictFirstList)



  def WriteSheet(self, writebook, k, v):
    sheet = writebook.add_sheet(k, cell_overwrite_ok=True)
    HEAD = [u'日期', u'总套数', u'平均总价', u'平均面积', u'平均单价', u'关注人数', u'带看次数', u'发布天数']
    for field in range(0, len(HEAD)):
      sheet.write(0, field, HEAD[field])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in xrange(1, len(v) + 1):
      sheet.write(row, 0, u'%s' % v[row - 1].date)
      sheet.write(row, 1, v[row - 1].total)
      sheet.write(row, 2, v[row - 1].total_price)
      sheet.write(row, 3, v[row - 1].avg_square)
      sheet.write(row, 4, v[row - 1].avg_price)
      sheet.write(row, 5, v[row - 1].avg_attention)
      sheet.write(row, 6, v[row - 1].avg_look)
      sheet.write(row, 7, v[row - 1].avg_release)

# =======================================================
if __name__ == '__main__':
  a = Analyze(IN_DIR, OUT_DIR)
  a.Traversal()
  a.Analyze()