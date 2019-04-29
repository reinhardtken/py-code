if __name__ == '__main__':
    import fake_spider.yjbg
    import fake_spider.lrb
    import fake_spider.zcfz
    import fake_spider.xjll
    import fake_spider.extra
    import query.query_extra
    import fake_spider.yysj

    #fake_spider.yjbg.run()
    #fake_spider.lrb.run()
    #fake_spider.zcfz.run()
    #fake_spider.xjll.run()
    query.query_extra.dropAll()
    fake_spider.extra.run()
    #fake_spider.yysj.run()