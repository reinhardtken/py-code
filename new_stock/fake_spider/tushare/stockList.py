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
from fake_spider import spider

#http://tushare.org/fundamental.html#id2
# code,代码
# name,名称
# industry,所属行业
# area,地区
# pe,市盈率
# outstanding,流通股本(亿)
# totals,总股本(亿)
# totalAssets,总资产(万)
# liquidAssets,流动资产
# fixedAssets,固定资产
# reserved,公积金
# reservedPerShare,每股公积金
# esp,每股收益
# bvps,每股净资
# pb,市净率
# timeToMarket,上市日期
# undp,未分利润
# perundp, 每股未分配
# rev,收入同比(%)
# profit,利润同比(%)
# gpr,毛利率(%)
# npr,净利润率(%)
# holders,股东人数
def getBasics():
  try:
    df = ts.get_stock_basics()
    df.rename(columns=TS.BASICS.KEY_NAME, inplace=True)
    # df.set_index(TS.BASICS.KEY_NAME['code'], inplace=True)
    # re.to_excel('/home/ken/workspace/tmp/stock_list.xls')
    return df
  except Exception as e:
    print(e)




# def genKeyCodeFunc():
#   # def keyCodeFunc(v, d):
#   #   return {const.MONGODB_ID: v, TS.BASICS.KEY_NAME['code']: v}
#
#   return lambda v, d: {const.MONGODB_ID: v, TS.BASICS.KEY_NAME['code']: v}


def saveDB(data: pd.DataFrame, handler=None):
  def callback(result):
    # handler.send_message(handler.project_name, result, self._date + '_' + result['_id'])
    pass

  re = util.updateMongoDB(data, util.genKeyCodeFunc(TS.BASICS.KEY_NAME['code']), TS.BASICS.DB_NAME, TS.BASICS.COLLECTION_NAME, True, callback)
  # util.everydayChange(re, 'gpfh')




if __name__ == '__main__':
  re = getBasics()
  saveDB(re)