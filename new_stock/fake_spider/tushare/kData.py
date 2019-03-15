# -*- encoding: utf-8 -*-

# sys
import json
# thirdpart
import pandas as pd
import tushare as ts

# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils
import const
import const.TS as TS
import setting

#http://tushare.org/classifying.html#id8
# code :股票代码
# name :股票名称
# date :日期
# weight:权重



def getLastK(code):
  end = util.today().strftime('%Y-%m-%d')
  start = util.weekAgo().strftime('%Y-%m-%d')
  try:
    df = ts.get_k_data(code, start=start, end=end)
    df.loc[:, 'date'] = pd.to_datetime(df.loc[:, 'date'])
    df.set_index('date', inplace=True)
    df.drop('code', axis=1, inplace=True)
    return df
  except Exception as e:
    print(e)



def getKData(code):
  try:
    df = ts.get_k_data(code)
    df.loc[:, 'date'] = pd.to_datetime(df.loc[:, 'date'])
    df.set_index('date', inplace=True)
    df.drop('code', axis=1, inplace=True)
    return df
  except Exception as e:
    print(e)




def saveDB(data: pd.DataFrame, code, handler=None):
  def callback(result):
    # handler.send_message(handler.project_name, result, self._date + '_' + result['_id'])
    pass

  re = util.updateMongoDB(data, util.genKeyCodeFunc('date'), TS.KData.DB_NAME, TS.KData.COLLECTION_D_HEAD + code, True, callback)
  # util.everydayChange(re, 'gpfh')


def run():
  STOCK_LIST = setting.currentStockList()
  for one in STOCK_LIST:
    re = getKData(one)
    saveDB(re, one)

if __name__ == '__main__':
  STOCK_LIST = setting.currentStockList()
  for one in STOCK_LIST:
    re = getKData(one)
    saveDB(re, one)