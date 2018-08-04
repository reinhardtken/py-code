# -*- coding: utf-8 -*-


#sys
import datetime

#thirdpart
import pandas as pd
from pymongo import MongoClient
#this project
if __name__ == '__main__':
    import sys
    sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import util
import util.utils
import const


STOCK_LIST = const.STOCK_LIST
KEY_NAME = const.CWSJ_KEYWORD.KEY_NAME



def QueryTop(top, code):
    client = MongoClient()
    db = client['stock']
    collection = db['cwsj-' + code]

    out = []

    cursor = collection.find()
    index = 0
    for c in cursor:
        c[KEY_NAME['date']] = datetime.datetime.strptime(c[KEY_NAME['date']], '%Y-%m-%d')
        out.append(c)
        print(c)
        index += 1
        if top != -1 and index > top:
            break

    df = pd.DataFrame(out)
    df.set_index(KEY_NAME['date'], inplace=True)
    return df



def dropAll():
    client = MongoClient()
    db = client['stock']
    for one in STOCK_LIST:
        collection = db['cwsj-' + one]
        collection.drop()


if __name__ == '__main__':
    # dropAll()
    df = QueryTop(-1, '000725')
    print(df)
    df.to_excel('/home/ken/workspace/tmp/out-000725.xls')
    # SaveData(re)
    pass