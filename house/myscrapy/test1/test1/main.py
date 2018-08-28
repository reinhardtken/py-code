from scrapy import cmdline

cmdList = [
# "scrapy crawl lianjia-bj",
# "scrapy crawl lianjia-sh",
# "scrapy crawl lianjia-sz",
"scrapy crawl lianjia-gz",
]
for one in cmdList:
  try:
    cmdline.execute(one.split())
  except Exception as e:
    print(e)
# cmdline.execute("scrapy crawl lianjia2 -s CLOSESPIDER_ITEMCOUNT=5".split())