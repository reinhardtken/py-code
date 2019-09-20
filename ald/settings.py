# -*- coding: utf-8 -*-

# Scrapy settings for ald project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ald'

SPIDER_MODULES = ['ald.spiders']
NEWSPIDER_MODULE = 'ald.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ald (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ald.middlewares.Test1SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'ald.middlewares.Test1DownloaderMiddleware': 543,
    'ald.middlewares.SeleniumMiddleware': 544,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
EXTENSIONS = {
  'ald.extensions.HooksasyncExtension': 100,
  #Address already in use
  #http://jinbitou.net/2016/08/18/1992.html
  #不能使用telnet console同时运行两个scrapy进程(scrapy shell)
  'scrapy.telnet.TelnetConsole': None,

}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
  'ald.pipelines.MongoPipeline': 300,
  'ald.pipelines.MongoPipelineALD':301
#   'ald.pipelines.MongoPipelineDetailDigest': 301,
#   'ald.pipelines.MongoPipelineDigest': 302,
# 'ald.pipelines.MongoPipelineTurnoverDetailDigest': 303,
#   'ald.pipelines.MongoPipelineTurnoverDigest': 304,
# 'ald.pipelines.MongoPipelineRentHouse': 305,
# 'ald.pipelines.MongoPipelineRentDetailDigest': 306,
#   'ald.pipelines.MongoPipelineRest': 307,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

def nowString():
  import datetime
  now = datetime.datetime.now()
  now = now.replace(microsecond=0)
  return now.strftime('%Y-%m-%d-%H-%M-%S')
#self setting
# filename = '/home/ken/workspace/tmp/log/' + nowString() + '.log'
filename = 'C:/workspace/tmp/' + nowString() + '.log'
# LOG_FILE = filename
LOG_LEVEL= 'WARNING'
# CHROME_DRIVER_PATH = r'/home/ken/prog/chromedriver_linux64/chrom/edriver'
CHROME_DRIVER_PATH = r'C:/prog/chromedriver_win32/chromedriver.exe'
PHANTOMJS_PATH = r'/home/ken/prog/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
SELENIUM_TIMEOUT = 20
PHANTOMJS_SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']