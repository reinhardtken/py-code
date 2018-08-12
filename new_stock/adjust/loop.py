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
  def before(self, data):
    pass

  def check(self, base, result):
    return False


class AdjustOPSimpleColumnCheck(AdjustOP):
  def baseColumns(self):
    return []

  def before(self, data):
    for one in self.columns():
      data.loc[:, one] = np.nan
    pass

  # def check2(self, baseBenchmark, resultBenchmark):
  #   def innerCheck(x):
  #     if np.isnan(x):
  #       return True
  #     elif math.fabs(x) < 0.000001:
  #       return True
  #
  #     return False
  #
  #   if len(self.columns()) != len(self.baseColumns()):
  #     return False
  #
  #   base_c = self.baseColumns()
  #   c = self.columns()
  #   for index in range(len(self.columns())):
  #     base = baseBenchmark.loc[:, base_c[index]]
  #     result = resultBenchmark.loc[:, c[index]]
  #     print('origin data!!!!')
  #     print(base)
  #     print('result data!!!!')
  #     print(result)
  #     diff = base - result
  #     print(diff)
  #     re = diff.map(innerCheck)
  #     print(re)
  #     if not re.all():
  #       redf = pd.DataFrame(data=re, columns=['diffValue'])
  #       out = redf.join(base).join(result)
  #       print(out)
  #       print(out.loc[lambda df: df.diffValue == False, :])
  #       return False
  #   else:
  #     return True

  def bypass(self, data, columns):
    return False


  def check(self, baseBenchmark, resultBenchmark):
    #https://blog.csdn.net/u010814042/article/details/76401133
    # args = []
    def innerCheck(x):
      try:
        benchmark = x.benchmark
        if isinstance(x.benchmark, str):
          benchmark = np.nan

        if not np.isnan(benchmark) and not np.isnan(x.result):
          if math.fabs(benchmark-x.result) < 0.000001:
            return pd.Series([True, benchmark, x.result], index=['check', 'benchmark', 'result'])
          else:
            return pd.Series([False, benchmark, x.result], index=['check', 'benchmark', 'result'])
        elif np.isnan(benchmark) and np.isnan(x.result):
          return pd.Series([True, benchmark, x.result], index=['check', 'benchmark', 'result'])
        else:
          return pd.Series([False, benchmark, x.result], index=['check', 'benchmark', 'result'])
      except Exception as e:
        print(e)
        return pd.Series([False, benchmark, x.result], index=['check', 'benchmark', 'result'])


    if len(self.columns()) < len(self.baseColumns()):
      return False

    base_c = self.baseColumns()
    c = self.columns()
    for index in range(len(self.baseColumns())):
      base = baseBenchmark.loc[:, base_c[index]]
      result = resultBenchmark.loc[:, c[index]]
      print('origin data!!!!')
      print(base)
      print('result data!!!!')
      print(result)
      redf = pd.DataFrame(data=base)#columns=['diffValue'], index=base.index)
      redf.rename(columns={base_c[index]: 'benchmark'}, inplace=True)
      redf = redf.join(result)
      redf.rename(columns={c[index]: 'result'}, inplace=True)
      print(redf)
      out = redf.apply(innerCheck, axis=1)
      print(out)
      out = out.loc[lambda df : df.check == False, :]
      if len(out.index) > 0:
        print('%s test : %s, %s not pass!!!'%(self.name(), base_c[index], c[index]))
        print(out)
        if not self.bypass(out, [base_c[index], c[index]]):
          return False

    else:
      return True

class AdjustLoop:
  def __init__(self):
    self._newColumns = []
    self._opList = []

  @property
  def columns(self):
    return self._newColumns

  def addOP(self, op):
    if isinstance(op, AdjustOP):
      self._newColumns.extend(op.columns())
      self._opList.append(op)

  def loop(self, data: pd.DataFrame):
    df = pd.DataFrame(columns=self._newColumns, index=data.index)
    # print(data)
    # print(df)
    data = data.join(df)
    # newDF = pd.DataFrame.merge(data, df)
    for one in self._opList:
      one.op(data)

    return data


  def verify(self, data: pd.DataFrame, benchmark: pd.DataFrame=None):
    if benchmark is None:
      benchmark = data.copy()

    for one in self._opList:
      one.before(data)
      one.op(data)
      suc = one.check(benchmark, data)
      if not suc:
        print('%s test has failed!!!'%(one.name()))
        break
    else:
      print('test all pass !!!')


  def genResult(self, data, ext=None):
    def inner(x):
      print(dir(x.loc[const.COMMON_ID].values))
      pass
    tmp = self._newColumns
    tmp.append(const.MONGODB_ID)
    if ext:
      tmp.extend(ext)
    df = pd.DataFrame(data=data.loc[:, tmp], index=data.index)
    # df[const.MONGODB_ID] = df.apply(inner, axis=1)
    # df[const.MONGODB_ID] = df.apply(lambda line : line[const.COMMON_ID].strftime('%Y-%m-%d'), axis=1)
    print(df)
    return df