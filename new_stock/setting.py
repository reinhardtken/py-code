import query.query_hs300
import const
import sys


def currentStockList():
  hs300 = query.query_hs300.queryCodeList()
  chose = const.STOCK_LIST
  one = set(chose)
  two = set(hs300)
  one.update(two)
  out = list(one)
  return out

def currentOS():
  if sys.platform == 'linux':
    return 'linux'
  else:
    return 'win'

CHROME_DRIVER_PATH = r'/home/ken/prog/chromedriver_linux64/chromedriver' if sys.platform == 'linux' else \
  ''
PHANTOMJS_PATH = r'/home/ken/prog/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'  if sys.platform == 'linux' else \
  ''

if __name__ == '__main__':
  out = currentStockList()