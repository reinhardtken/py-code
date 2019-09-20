# -*- coding: utf-8 -*-
# import subprocess
import time
import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.spiderloader import SpiderLoader



if __name__ == "__main__":
  #https://blog.csdn.net/qq_40755643/article/details/80253395
  #https://segmentfault.com/q/1010000008578604
  allow = set(["zy-esf-cd",
               "zy-esf-cq",

               # "lianjia-tj",
                    # "lianjia-xm",
                    # "lianjia-hf",
               ])

  allow2 = set([
    "lianjia-cj-bj",
# "lianjia-cj-sz",
# "lianjia-cj-gz",
# "lianjia-cj-hz",
# "lianjia-cj-nj",
# "lianjia-cj-cs",
# "lianjia-cj-wh",
# "lianjia-cj-tj",
# "lianjia-cj-zz",
#"lianjia-cj-xa",
#"lianjia-cj-cd",
#"lianjia-cj-su",
#  "lianjia-cj-cq",
# "lianjia-cj-xm",
# "lianjia-cj-hf",
    ])
  process = CrawlerProcess(get_project_settings())
  runner = CrawlerRunner(get_project_settings())
  # runner.crawl()
  sloader = SpiderLoader(get_project_settings())
  scheduler = TwistedScheduler()
  hour = 1
  for spidername in sloader.list():
    # scheduler.add_job(task, 'cron', minute="*/20")
    if spidername in allow:
      #https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html
      # scheduler.add_job(process.crawl, 'cron', args=[spidername], hour="*/" + str(hour))
      # scheduler.add_job(func=aps_test, args=('定时任务',), trigger='cron', second='*/5')
      # scheduler.add_job(func=aps_test, args=('一次性任务',),
      #                   next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=12))
      # scheduler.add_job(func=aps_test, args=('循环任务',), trigger='interval', seconds=3)
      print(spidername)
      scheduler.add_job(process.crawl, trigger='date', args=[spidername],
                        run_date=datetime.datetime(2018, 9, 10, hour, 0, 0))
      # scheduler.add_job(process.crawl, trigger='cron', args=[spidername],
      #                   year='*', month='*', day=9, week='*', day_of_week='*', hour=hour, minute=20, second=0)
      # scheduler.add_job(process.crawl, args=[spidername], next_run_time=datetime.datetime.now() + datetime.timedelta(hours=4))
      hour += 1

  scheduler.start()
  process.start(False)
  try:
    while True:
      time.sleep(2)
  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()