# -*- coding: utf-8 -*-
# import subprocess
import time
import datetime

from scrapy.crawler import CrawlerProcess
# from spiders.egov import EgovSpider
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.spiderloader import SpiderLoader



if __name__ == "__main__":
  #https://blog.csdn.net/qq_40755643/article/details/80253395
  #https://segmentfault.com/q/1010000008578604
  allow = set(["lianjia-cq",
                    "lianjia-xm",
                    "lianjia-hf",])

  allow2 = set([
    # "scrapy crawl lianjia-bj",
#"scrapy crawl lianjia-sh",
"lianjia-cj-sz",
# "lianjia-cj-gz",
# "lianjia-cj-hz",
# "lianjia-cj-nj",
"lianjia-cj-cs",
# "lianjia-cj-wh",
# "lianjia-cj-tj",
# "lianjia-cj-zz",
# "lianjia-cj-xa",
# "lianjia-cj-cd",
# "lianjia-cj-su",
# "lianjia-cj-cq",
# "lianjia-cj-xm",
# "lianjia-cj-hf",
    ])
  process = CrawlerProcess(get_project_settings())
  sloader = SpiderLoader(get_project_settings())
  scheduler = TwistedScheduler()
  hour = 3
  for spidername in sloader.list():
    # scheduler.add_job(task, 'cron', minute="*/20")
    if spidername in allow2:
      #https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html
      # scheduler.add_job(process.crawl, 'cron', args=[spidername], hour="*/" + str(hour))
      # scheduler.add_job(func=aps_test, args=('定时任务',), trigger='cron', second='*/5')
      # scheduler.add_job(func=aps_test, args=('一次性任务',),
      #                   next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=12))
      # scheduler.add_job(func=aps_test, args=('循环任务',), trigger='interval', seconds=3)
      scheduler.add_job(process.crawl, 'cron', args=[spidername], next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=12))
      hour += 2

  scheduler.start()
  process.start(False)
  try:
    while True:
      time.sleep(2)
  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()