import adjust.cwsj_manager
import fake_spider.lrb
import fake_spider.zcfz
import fake_spider.xjll
import fake_spider.extra
import fake_spider.yysj
import fake_spider.tushare.kData
import fake_spider.zgb3
import query.query_stock_list
import fake_spider.tushare.stockList
import fake_spider.cwsj


def run():
  adjust.cwsj_manager.testOne('002475')


if __name__ == '__main__':
  # fake_spider.cwsj.run()
  # fake_spider.tushare.stockList.saveDB(fake_spider.tushare.stockList.getBasics())
  # query.query_stock_list.queryAll()
  # fake_spider.zgb3.run()
  adjust.cwsj_manager.testOne('002475')
  fake_spider.tushare.kData.run()
  run()