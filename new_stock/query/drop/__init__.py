# -*- coding: utf-8 -*-

# sys
from inspect import signature

# thirdpart
import pandas as pd
from pymongo import MongoClient

# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils
import const




def dropAll(dbName, head):
  client = MongoClient()
  db = client[dbName]
  print(dir(db))
  names = db.collection_names()
  print(signature(db.drop_collection).parameters)
  print(names)
  for one in names:
    if head == '#' or one.startswith(head):
      collection = db[one]
      collection.drop()



def allGPFH():
  dropAll('stock', 'gpfh-')


def allMacroMX():
  dropAll('stock', 'macro-M')


def allCWSJ():
  dropAll('stock', 'cwsj-')

def allYJYG():
  dropAll('stock', 'yjyg-')

def allEverydat():
  dropAll('stock-everyday', '2018')

def allHS300():
  dropAll('stock', 'hs300_stock_list')


def allKData():
  dropAll('stock_kdata', '#')


if __name__ == '__main__':
  allKData()
  # allHS300()
  # allEverydat()
  # allYJYG()
  # allGPFH()
  # allMacroMX()
  # allCWSJ()
  pass