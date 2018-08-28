from scrapy import cmdline

cmdline.execute("scrapy crawl lianjia".split())
# cmdline.execute("scrapy crawl lianjia2 -s CLOSESPIDER_ITEMCOUNT=5".split())