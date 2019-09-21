
import sys
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
# 'scrapy crawl lianjia-esf-sh'
# 'scrapy crawl lianjia-esf-cs'

   # 'scrapy crawl lianjia-esf-building'
'scrapy crawl lianjia-esf-bj'
]  


#添加当前项目的绝对地址
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#执行 scrapy 内置的函数方法execute，  使用 crawl 爬取并调试，最后一个参数jobbole 是我的爬虫文件名



for one in cmdList:
  try:
    cmdline.execute(one.split())
    print(one)
  except Exception as e:
    print(e)
cmdline.execute("scrapy crawl lianjia2 -s CLOSESPIDER_ITEMCOUNT=5".split())


# def run(param):
#   try:
#     cmd = 'scrapy crawl ' + param
#     print('cmdline : ' + cmd)
#     cmdline.execute(cmd.split())
#   except Exception as e:
#     print(e)
#
#
# if __name__ == '__main__':
#   import sys
#   sys.path.append('/home/ken/workspace/code/self/github/py-code/house')
#   if len(sys.argv) >= 2:
#     param = sys.argv[1]
#     run(param)