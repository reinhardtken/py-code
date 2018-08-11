# -*- coding: utf-8 -*-


# sys
import datetime

# thirdpart
import pandas as pd
import pymongo
from pymongo import MongoClient

# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils
import const



def Query(dates, code):
  out = []
  client = MongoClient()
  db = client['stock']
  for date in dates:
    collection = db['yjyg-' + date]  # -2018-09-30']
    cursor = collection.find({'_id': code})
    for c in cursor:
      c[const.CWSJ_KEYWORD.KEY_NAME['date']] = datetime.datetime.strptime(date, '%Y-%m-%d')
      c.pop('_id')
      out.append(c)

  df = pd.DataFrame(out)
  if len(df.index) > 0:
    df.set_index(const.CWSJ_KEYWORD.KEY_NAME['date'], inplace=True)
  return df


if __name__ == '__main__':
  out = Query(['2018-09-30', '2018-06-30', '2018-03-31'], '002415')
  pass