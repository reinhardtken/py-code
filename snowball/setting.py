import query.query_hs300
import const
import sys
import get_list


#out pathh and list path
PATH = r'C:\workspace\tmp/'
list_path = r'C:\workspace\tmp/'
yjyg_list = ['2019-09-30',
             '2019-06-30',
             '2019-03-31']


def currentStockList():
  hs300 = query.query_hs300.queryCodeList()
  chose = get_list.get_portfolio()
  zz500 = get_list.get_zz500()
  zxbz = get_list.get_zxbz()
  cybz = get_list.get_cybz()
  AI = get_list.get_AI()
  guangdong = get_list.get_guangdong()
  medicine = get_list.get_medicine()
  all = get_list.get_all()
  one = set(chose)
  two = set(hs300)
  three = set(zz500)
  four = set(zxbz)
  five = set(cybz)
  six = set(AI)
  seven = set(guangdong)
  eight = set(medicine)
  nine = set(all)
  one.update(two)
  one.update(three)
  one.update(four)
  one.update(five)
  one.update(six)
  one.update(seven)
  one.update(eight)
  one.update(nine)
  out = list(one)
  return out

#fanancial report data stock list
F_data_stock_list_name = 'portfolio'
def f_data_stocklist():
    #return ['600571']
    #out = query.query_hs300.queryCodeList()
    out = get_list.get_portfolio()
    #out = get_list.get_all()
    #out = currentStockList()
    return out

#stock_list for cwsj_manager
def stock_list():
  return [(currentStockList(), PATH + '/out-all.xlsx'),
              (query.query_hs300.queryCodeList(), PATH + '/out-hs300.xlsx'),
              (get_list.get_portfolio(), PATH + '/out-portfolio.xlsx'),
              (get_list.get_zz500(), PATH + '/out-zz500.xlsx'),
              (get_list.get_zxbz(), PATH + '/out-zxbz.xlsx'),
              (get_list.get_cybz(), PATH + '/out-cybz.xlsx'),
              (get_list.get_AI(), PATH + '/out-AI.xlsx'),
              (get_list.get_guangdong(), PATH + '/out-guangdong.xlsx'),
              (get_list.get_medicine(), PATH + '/out-medicine.xlsx')]

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