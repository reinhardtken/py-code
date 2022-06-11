#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import pyquery

from selenium import webdriver
import setting
# CHROME_DRIVER_PATH = r'/home/ken/prog/chromedriver_linux64/chromedriver'
# PHANTOMJS_PATH = r'/home/ken/prog/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'


class Response:
  def __init__(self):
    self.ok = False
    self.content = None
    self.url = None
    self.save = {}

  def doc(self, k):
    pq = pyquery.PyQuery(self.content)
    if not k:
      return pq
    else:
      return pq(k)


class FakeSpider():

  def __init__(self):
    self.__task_list = []
    self.project_name = 'FakeSpider'


  def param(self):
    return None

  def crawl(self, url, **kwargs):
    if isinstance(url, str):
      self.__task_list.append((url, kwargs))
    elif isinstance(url, list):
      for u in url:
        self.__task_list.append((u, kwargs))
    else:
      return

  def send_message(self, project, msg, url=None):
    self.on_message(project, msg)

  def run(self):
    print(f'start task total: {len(self.__task_list)}')
    total = len(self.__task_list)
    counter = 0
    while (True):
      notEmpty = False
      tempTaskList = self.__task_list.copy()
      self.__task_list.clear()
      for task in tempTaskList:
        if counter % 10 == 0:
          print(f'start task progress: {counter}/{total}  ####################################')
        counter += 1

        notEmpty = True
        s = requests.Session()
        s.mount('http://', requests.adapters.HTTPAdapter(max_retries=5))
        s.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))

        callback = None
        save = {}
        header = None
        param = None
        url = task[0]
        fetch_js = False
        if task[1].get('callback'):
          callback = task[1]['callback']
        if task[1].get('headers'):
          header = task[1]['headers']
        if task[1].get('save'):
          save = task[1].get('save')
        if task[1].get('fetch_type'):
          fetch_js = True
        if task[1].get('param'):
          param = task[1].get('param')

        response = Response()
        response.url = url

        r = None
        if fetch_js == False:
          try:
            r = s.get(url, headers=header, timeout=10, params=param)
            if r.status_code == 200:
              try:
                response.ok = True
                response.content = r.content
                response.save = save
                callback(response)
              except Exception as e:
                print(e)
            else:
              print('net Error', r.status_code)
          except requests.ConnectionError as e:
            print('Error', e.args)

        else:
          client = None
          if setting.currentOS() == 'linux':
            # headless
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            client = webdriver.Chrome(setting.CHROME_DRIVER_PATH, chrome_options=options)
          else:
            client = webdriver.PhantomJS(executable_path =setting.PHANTOMJS_PATH, service_args=['--load-images=false', '--disk-cache=true'])
            
          client.get(url)
          print(client.current_url)
          r = client.page_source

          try:
            response.ok = True
            response.content = r
            response.save = save
            callback(response)
          except Exception as e:
            print(e)

      if notEmpty and len(self.__task_list):
        continue
      else:
        break

  #########################################################################
  def on_start(self):
    self.crawl(self.url(), headers=self.header(), param=self.param(), callback=self.processFirstPage)
