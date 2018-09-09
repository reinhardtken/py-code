# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time
from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger

class Test1SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Test1DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # for k, v in spider.headers.items():
        #   request.headers[k] = v

        ua = random.choice(self.user_agent_list)
        if ua:
          # request.headers.setdefault('User-Agent', ua)
          request.headers['User-Agent'] = ua
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

###################################################################
class SeleniumMiddleware():
  def __init__(self, timeout=None, service_args=[], executable_path=None):
    self.logger = getLogger(__name__)
    self.timeout = timeout
    self.executable_path = executable_path
    self.timeoutCounter = 0
    self.innerInit()

  def __del__(self):
    self.innerDestroy()


  def innerInit(self):
    # headless
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    prefs = {
      'profile.default_content_setting_values': {
        'images': 2
      }
    }
    options.add_experimental_option('prefs', prefs)
    #options.add_argument('lang=zh_CN.UTF-8')
    #易居的网站会根据ua返回数据，默认会返回移动站数据，强制设置pcua后则不返回数据，问题尚未解决
    #https://yijufangyou1.anjuke.com/gongsi-esf/
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"')
    # options.add_argument(
    #   'user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36"')

    #try:
    self.browser = webdriver.Chrome(executable_path=self.executable_path, chrome_options=options)
    # self.browser = webdriver.PhantomJS(executable_path=executable_path, service_args=service_args)
    self.browser.set_window_size(1400, 700)
    self.browser.set_page_load_timeout(self.timeout)
    # self.wait = WebDriverWait(self.browser, self.timeout)
    #except Exception as e:
      #print(e)
    pass

  def innerDestroy(self):
    try:
      if self.browser is not None:
        self.browser.close()
    except Exception as e:
      print(e)
    pass

  def waitLogic(self, spider, requestURL):
    url = None
    for i in range(3):
      self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      wait = WebDriverWait(self.browser, 2)
      try:
        url = wait.until(EC.presence_of_element_located((By.XPATH, spider.xpath['anchor'])))
        # url = wait.until(EC.presence_of_element_located((By.XPATH, spider.processAnchor(requestURL))))
        if url is not None:
          break
      except Exception as e:
        print(e)
    else:
      self.logger.warning('SeleniumMiddleware wait failed!!! %s'%(self.browser.current_url))
      # content = self.browser.page_source
      # data = content.decode('utf-8')
      pass


  def process_request(self, request, spider):
    """
    用PhantomJS抓取页面
    :param request: Request对象
    :param spider: Spider对象
    :return: HtmlResponse
    """
    self.logger.debug('ChromeDriver is Starting')

    if self.timeoutCounter >= 1:
      self.timeoutCounter = 0
      self.innerDestroy()
      self.innerInit()

    try:
      # print(dir(self.browser))
      self.browser.get(request.url)
      self.waitLogic(spider, request.url)
      return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                          status=200)
    except TimeoutException as e:
      print(e)
      self.logger.warning('TimeoutException: %s' % str(e))
      self.timeoutCounter += 1

      return HtmlResponse(url=request.url, status=500, request=request)
    except Exception as e:
      print(e)
      self.logger.warning('Exception: %s' % str(e))
      return HtmlResponse(url=request.url, status=501, request=request)

  @classmethod
  def from_crawler(cls, crawler):
    return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
               #service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'),
               executable_path=crawler.settings.get('CHROME_DRIVER_PATH'))