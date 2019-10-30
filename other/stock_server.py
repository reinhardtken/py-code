
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import tushare as ts
import json


def GetPrice():
  print("GetPrice run...")
  out = {}
  try:
    df = ts.get_index()
    # print(df)
    # 这里有问题，应该是和昨天收盘比涨跌，不是今天开盘
    AStock = df.loc[df.code == '000001']
    
    out['code'] = AStock.loc[0, 'code']
    out['name'] = AStock.loc[0, 'name']
    out['close'] = AStock.loc[0, 'close']
    out['open'] = AStock.loc[0, 'open']
    out['preclose'] = AStock.loc[0, 'preclose']
    out['error'] = 0
    
    # re.code = AStock.loc[0, 'code']
    # re.name = AStock.loc[0, 'name']
    # re.closePrice = AStock.loc[0, 'close']
    # re.openPrice = AStock.loc[0, 'open']
    # re.error = 0
  except Exception as e:
    print(e)
    out['error'] = -1

  out2  = json.dumps(out)
  return out2

class StockPriceHandler(tornado.web.RequestHandler):
    def get(self):
      out = GetPrice()
      self.write(out)

if __name__ == "__main__":
    print("version=1.0.2                     stock server run...")
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/stock_price", StockPriceHandler)
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()