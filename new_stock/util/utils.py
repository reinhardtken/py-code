#!/usr/bin/env python
# -*- encoding: utf-8 -*-


def genchangeKeyFunc(newKey):
  def changeKey(k, v):
    if k in newKey:
      return newKey[k], v
    return k, v

  return changeKey


def genCutDateFunc(key):
  def cutDate(k, v):
    if k in key:
      return k, v[:10]
    return k, v

  return cutDate


def genString2NumberFunc(key):
  def tryFloat(v):
    try:
      return True, float(v)
    except ValueError as e:
      return False, v

  def toNumber(k, v):
    if k in key:
      succ, v = tryFloat(v)
      if succ == True:
        return k, v
      newV = v.replace(',', '')
      succ, v = tryFloat(newV)
      if succ == True:
        return k, v
      if v[-1] == '亿':  # 938亿
        _, v = tryFloat(v[:-1]) * 100000000


    return k, v

  return toNumber


def genEatFunc(key):
  def eat(k, v):
    if k in key:
      return k, v
    else:
      return None, None

  return eat


def threeOP(k1, k2, k3):
  return [genCutDateFunc(k1), genString2NumberFunc(k2), genchangeKeyFunc(k3)]


def fourOP(k1, k2, k3, k4):
  return [genCutDateFunc(k1), genString2NumberFunc(k2), genEatFunc(k3), genchangeKeyFunc(k4)]


def dealwithData(data, itemList):
  out = {}
  for k, v in data.items():
    for op in itemList:
      k, v = op(k, v)

    if k is not None:
      out[k] = v

  return out



def readList():
  import xlrd

  workbook = xlrd.open_workbook('/home/ken/workspace/tmp/in.xlsx')

  sheet = workbook.sheet_by_name('股票池')
  '''
  sheet.nrows　　　　sheet的行数
  sheet.row_values(index)　　　　返回某一行的值列表
　　sheet.row(index)　　　　返回一个row对象，可以通过row[index]来获取这行里的单元格cell对象'''
  nrows = sheet.nrows
  out = []
  for index in range(1, nrows):
    print(nrows)
    row = sheet.row(index)
    out.append(row[0].value)

  for one in out:
    print('"' + str(one) + '",')
