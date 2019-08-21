

from scrapy import cmdline

cmdList = [
# "scrapy crawl lianjia-digest",
# "scrapy crawl lianjia-bj",
#"scrapy crawl lianjia-sh",
#"scrapy crawl lianjia-sz",
#"scrapy crawl lianjia-gz",
#"scrapy crawl lianjia-hz",
#"scrapy crawl lianjia-nj",
# "scrapy crawl lianjia-cs",
# "scrapy crawl lianjia-wh",
# "scrapy crawl lianjia-tj",
#"scrapy crawl lianjia-zz",
#"scrapy crawl lianjia-xa",
# "scrapy crawl lianjia-cd",
# "scrapy crawl lianjia-su",
# "scrapy crawl lianjia-cq",
# "scrapy crawl lianjia-xm",
# "scrapy crawl lianjia-hf",

# "scrapy crawl lianjia-cj-bj",
# "scrapy crawl lianjia-cj-xa",
# "scrapy crawl lianjia-cj-digest",

# "scrapy crawl wiwj-esf-hz",
'scrapy crawl lianjia-esf-cs'
]

for one in cmdList:
  try:
    cmdline.execute(one.split())
    print(one)
  except Exception as e:
    print(e)
# cmdline.execute("scrapy crawl lianjia2 -s CLOSESPIDER_ITEMCOUNT=5".split())