# -*- coding: utf-8 -*-
# import subprocess
import time


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
  process = CrawlerProcess(get_project_settings())
  sloader = SpiderLoader(get_project_settings())
  scheduler = TwistedScheduler()
  hour = 3
  for spidername in sloader.list():
    # scheduler.add_job(task, 'cron', minute="*/20")
    if spidername in allow:
      #https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html
      scheduler.add_job(process.crawl, 'cron', args=[spidername], hour="*/" + str(hour))
      hour += 1

  scheduler.start()
  process.start(False)
  try:
    while True:
      time.sleep(2)
  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()