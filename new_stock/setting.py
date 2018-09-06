import query.query_hs300
import const


def currentStockList():
  hs300 = query.query_hs300.queryCodeList()
  chose = const.STOCK_LIST
  one = set(chose)
  two = set(hs300)
  one.update(two)
  out = list(one)
  return out



if __name__ == '__main__':
  out = currentStockList()