#!/usr/bin/env python
# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-


import xlwt

import xlrd
import types
import pandas as pd



#################################################################################
if __name__ == '__main__':
  path = '/home/ken/workspace/tmp/test2.xlsx'
  df = pd.read_excel(path)
  g = df.groupby('日期')
  for k,v in g:
    print(k)
    # print(type(v))
    # print(v)
    # print(v.sum())
    sum = v.loc[:, ['手机数量']].sum()
    # print(type(sum))
    # print(sum)
    # print(sum['手机数量'])
    total = sum['手机数量']
    print(total)
    v['percent'] = v.apply(lambda x: x['手机数量'] / total, axis=1)
    # print(v)
    # v.sort_values(by=['percent'], ascending=False, inplace=True)
    v.sort_values(by=['app个数'], ascending=True, inplace=True)
    v['cum'] = v['percent'].cumsum()
    # print(v)
    v.to_excel('/home/ken/workspace/tmp/' + str(k) + '.xlsx')
    pass

  pass