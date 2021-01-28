
if __name__ == '__main__':
    import F_data_to_db
    import F_data_out

    #use it to create stockList and hs300 when the first time and mongodb is empty
    #import fake_spider.tushare.hs300
    #fake_spider.tushare.hs300.saveDB(fake_spider.tushare.hs300.getHS300())
    #import fake_spider.tushare.stockList
    #fake_spider.tushare.stockList.saveDB(fake_spider.tushare.stockList.getBasics())

    #run main program
    F_data_to_db.run()
    F_data_out.run()