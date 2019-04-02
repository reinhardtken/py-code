import query.query_hs300
import const
import sys
import get_list


#out pathh and list path
PATH = r'd:/stock_python/out/'
list_path = r'd:/stock_python/list/'
yjyg_list = ['2019-06-30',
             '2019-03-31',
             '2018-12-31',
             '2018-09-30']

#stock_list for cwsj_manager
stock_list = [(query.query_hs300.queryCodeList(), PATH + '/out-hs300.xlsx'),
              (get_list.get_portfolio(), PATH + '/out-portfolio.xlsx'),
              (get_list.get_zz500(), PATH + '/out-zz500.xlsx'),
              (get_list.get_zxbz(), PATH + '/out-zxbz.xlsx'),
              (get_list.get_cybz(), PATH + '/out-cybz.xlsx'),
              (get_list.get_AI(), PATH + '/out-AI.xlsx'),
              (get_list.get_guangdong(), PATH + '/out-guangdong.xlsx'),
              (get_list.get_medicine(), PATH + '/out-medicine.xlsx')]

def currentStockList():
  hs300 = query.query_hs300.queryCodeList()
  chose = get_list.get_portfolio()
  zz500 = get_list.get_zz500()
  zxbz = get_list.get_zxbz()
  cybz = get_list.get_cybz()
  AI = get_list.get_AI()
  guangdong = get_list.get_guangdong()
  medicine = get_list.get_medicine()
  one = set(chose)
  two = set(hs300)
  three = set(zz500)
  four = set(zxbz)
  five = set(cybz)
  six = set(AI)
  seven = set(guangdong)
  eight = set(medicine)
  one.update(two)
  one.update(three)
  one.update(four)
  one.update(five)
  one.update(six)
  one.update(seven)
  one.update(eight)
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