# -*- coding: utf-8 -*-

# sys
import math

# thirdpart
import pandas as pd
import numpy as np
# this project
if __name__ == '__main__':
  import sys

  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
##########################
import const



class AdjustOP:
  def columns(self):
    return []

  def op(self, data):
    pass

  def name(self):
    return self.__class__.__name__

  #for test
  def baseColumns(self):
    return []

  def bofore(self, data):
    pass

  def check(self, base, result):
    return True


class AdjustOPSimpleColumnCheck(AdjustOP):
  def before(self, data):
    for one in self.columns():
      data.loc[:, one] = np.nan
    pass

  def check(self, base, result):
    def innerCheck(x):
      if np.isnan(x):
        return True
      elif math.fabs(x) < 0.000001:
        return True

      return False

    if len(self.columns()) != len(self.baseColumns()):
      return False

    base_c = self.baseColumns()
    c = self.columns()
    for index in range(len(self.columns())):
      base = base.loc[:, base_c[index]]
      result = result.loc[:, c[index]]
      print(base)
      print(result)
      diff = base - result
      print(diff)
      re = diff.map(innerCheck)
      print(re)
      if not re.all():
        return False
    else:
      return True



class AdjustLoop:
  def __init__(self):
    self._newColumns = []
    self._opList = []

  def addOP(self, op):
    if isinstance(op, AdjustOP):
      self._newColumns.extend(op.columns())
      self._opList.append(op)

  def loop(self, data: pd.DataFrame):
    df = pd.DataFrame(columns=self._newColumns, index=data.index)
    print(data)
    print(df)
    data.join(df)
    # newDF = pd.DataFrame.merge(data, df)
    for one in self._opList:
      one.op(data)

    return data


  def verify(self, data: pd.DataFrame):
    newData = data.copy()
    for one in self._opList:
      one.before(newData)
      one.op(newData)
      suc = one.check(data, newData)
      if not suc:
        print('%s test has failed!!!'%(one.name()))
        break
    else:
      print('test all pass !!!')


  def genResult(self, data):
    tmp = self._newColumns
    tmp.append(const.MONGODB_ID)
    df = pd.DataFrame(data=data.loc[:, tmp], index=data.index)
    print(df)
    return df