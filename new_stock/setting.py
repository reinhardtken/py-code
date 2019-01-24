import query.query_hs300
import const
import sys
import get_list


#out pathh and list path
PATH = r'd:/stock_python/out/'
list_path = r'd:/stock_python/list/'

#stock_list for cwsj_manager
stock_list = [(query.query_hs300.queryCodeList(), PATH + '/out-hs300.xls'),
              (const.STOCK_LIST, PATH + '/out-portfolio.xls'),
              (get_list.get_zz500(), PATH + '/out-zz500.xls'),
              (get_list.get_zxbz(), PATH + '/out-zxbz.xls'),
              (get_list.get_cybz(), PATH + '/out-cybz.xls')]

def currentStockList():
  hs300 = query.query_hs300.queryCodeList()
  chose = const.STOCK_LIST
  zz500 = get_list.get_zz500()
  zxbz = get_list.get_zxbz()
  cybz = get_list.get_cybz()
  one = set(chose)
  two = set(hs300)
  three = set(zz500)
  four = set(zxbz)
  five = set(cybz)
  one.update(two)
  one.update(three)
  one.update(four)
  one.update(five)
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