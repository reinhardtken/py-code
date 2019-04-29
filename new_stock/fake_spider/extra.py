#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-07-28 04:28:42
# Project: gpfh


# sys
import json
import random
import time
# thirdpart
import pandas as pd
from requests.models import RequestEncodingMixin

encode_params = RequestEncodingMixin._encode_params

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
from fake_spider import spider
import query.query_cwsj
import query.query_yjyg
import query.query_stock_list
import query.query_kdata
import query.query_lrb
import query.query_zcfz
import query.query_yjbg
import query.query_xjll



MONGODB_ID = const.MONGODB_ID
DB_NAME = const.EXTRA_KEYWORD.DB_NAME
COLLECTION_HEAD = const.EXTRA_KEYWORD.COLLECTION_HEAD

STOCK_LIST = setting.currentStockList()
# STOCK_LIST = ['000636']




class Handler:
  crawl_config = {
  }

  def on_start(self):
    pass



  def saveDB(self, data: pd.DataFrame, key):
    def callback(result):
      self.send_message(self.project_name, result, key + '_' + result[MONGODB_ID])

    util.saveMongoDB(data, util.genEmptyFunc(), DB_NAME, COLLECTION_HEAD + key, callback)
    # util.updateMongoDB(data, util.genKeyIDFunc(key), DB_NAME, COLLECTION_NAME, False, callback)


  def run(self):
    for code in STOCK_LIST:
      #zcfz.'应收账款增长率/lrb.收入增长率'
      #zcfz.存货增长率/lrb.收入增长率

      df = query.query_lrb.QueryTop(-1, code)
      df2 = query.query_zcfz.QueryTop(-1, code)
      df = df.loc[:, [const.LRB_KEYWORD.KEY_NAME['tystz'], ] ]
      df2 = df2.loc[:, [const.ZCFZ_KEYWORD.KEY_NAME['accountrec_tb'], const.ZCFZ_KEYWORD.KEY_NAME['inventory_tb']] ]

      #join是为了对齐index，怕存在index不齐的情况
      df3 = df2.join(df, how='outer')
      print(df3)
      df3.sort_index(inplace=True, ascending=False)
      #丢弃空行
      df3.dropna()

      # xjll.经营活动产生的现金流量净额/yjbg.营业收入
      # xjll.每股经营现金流量/stock_list.总股本
      df = query.query_xjll.QueryTop(-1, code)
      df2 = query.query_yjbg.QueryTop(-1, code)
      df = df.loc[:, [const.XJLL_KEYWORD.KEY_NAME['netoperatecashflow'], ]]
      df2 = df2.loc[:, [const.YJBG_KEYWORD.KEY_NAME['totaloperatereve'], ]]
      # basicInfo = query.query_stock_list.queryOne(code)
      zgb = query.query_stock_list.queryZgb(code)#basicInfo[const.TS.BASICS.KEY_NAME['zgb']]
      df4 = df2.join(df, how='outer')
      print(df4)
      df4.sort_index(inplace=True, ascending=False)
      df4.dropna()

      df5 = df4.join(df3, how='outer')
      df5['zgb'] = zgb
      df5.dropna()
      print(df5)

      # zcfz.'应收账款增长率/lrb.收入增长率'
      df5[const.EXTRA_KEYWORD.KEY_NAME['yszkzzl_srzzl']] = df5[const.ZCFZ_KEYWORD.KEY_NAME['accountrec_tb']] / \
                                                           df5[const.LRB_KEYWORD.KEY_NAME['tystz']]
      # zcfz.存货增长率/lrb.收入增长率
      df5[const.EXTRA_KEYWORD.KEY_NAME['chzzl_srzzl']] = df5[const.ZCFZ_KEYWORD.KEY_NAME['inventory_tb']] / \
                                                           df5[const.LRB_KEYWORD.KEY_NAME['tystz']]
      # xjll.经营活动产生的现金流量净额/yjbg.营业收入
      df5[const.EXTRA_KEYWORD.KEY_NAME['jyhdcsdxjllje_yysr']] = df5[const.XJLL_KEYWORD.KEY_NAME['netoperatecashflow']] / \
                                                         df5[const.YJBG_KEYWORD.KEY_NAME['totaloperatereve']]
      # xjll.每股经营现金流量/stock_list.总股本
      df5[const.EXTRA_KEYWORD.KEY_NAME['jyhdcsdxjllje_zgb']] = df5[const.XJLL_KEYWORD.KEY_NAME['netoperatecashflow']] / \
                                                                zgb

      df5 = df5.loc[:, [const.EXTRA_KEYWORD.KEY_NAME['yszkzzl_srzzl'],
                        const.EXTRA_KEYWORD.KEY_NAME['chzzl_srzzl'],
                        const.EXTRA_KEYWORD.KEY_NAME['jyhdcsdxjllje_yysr'],
                        const.EXTRA_KEYWORD.KEY_NAME['jyhdcsdxjllje_zgb']] ]
      df5[const.MONGODB_ID] = df5.index.values
      print(df5)
      self.saveDB(df5, code)



  def saveDB(self, data: pd.DataFrame, key):
    util.saveMongoDB(data, util.genEmptyFunc(), DB_NAME, COLLECTION_HEAD + key, None)


def run():
  gpfh = Handler()
  gpfh.on_start()
  gpfh.run()


if __name__ == '__main__':
  gpfh = Handler()
  gpfh.on_start()
  gpfh.run()
