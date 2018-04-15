# -*- coding: utf-8 -*-
#!/usr/bin/env python



# -*- coding: utf-8 -*-

import urllib2
import urlparse
import bs4
import xlwt
import time
import datetime
from selenium import webdriver

def TodayString():
  today = datetime.date.today()
  return today.strftime(u"%Y-%m-%d")
#=====================================================================

BEIJIN_HEAD = 'https://bj.lianjia.com'
CS_HEAD = 'https://cs.lianjia.com'
SZ_HEAD = 'https://sz.lianjia.com'
HZ_HEAD = 'https://hz.lianjia.com'
XA_HEAD = 'https://xa.lianjia.com'
OUTPATH = 'C:/workspace/text'
CHROME_DRIVER_PATH = 'C:/workspace/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(CHROME_DRIVER_PATH)




class OneJob:
  ERSHOUFANG = 1
  DITIEFANG = 2
  DISTRICTS = 2

  CS_DISTRICTS = 2
  CS_DITIEFANG = 2

  SZ_DISTRICTS = 2
  SZ_DITIEFANG = 2

  HZ_DISTRICTS = 2
  HZ_DITIEFANG = 2

  XA_DISTRICTS = 2
  XA_DITIEFANG = 2

  def __init__(self, title, head, url, pattern):
    self.title = title
    self.head = head
    self.url = url
    #下一页的模式
    self.url_pattern = pattern


  def OnePath(self, first, index):
    return self.head + first

  def TwoPath(self, first, index):
    slash_index = 0
    for i in range(0, 2):
      slash_index = first.find('/', slash_index + 1)
    else:
      head = first[:slash_index + 1]
      tail = first[slash_index + 1:]
      return self.head + head + 'pg' + str(index) + tail

  def ThreePath(self, first, index):
    return self.head + first + 'pg' + str(index)

  def NextPageURL(self, first, index):
    if self.url_pattern == OneJob.ERSHOUFANG:
      if index == 1:
        return self.OnePath(first, index)
      else:
        return self.head + first.replace('/ershoufang/', '/ershoufang/pg' + str(index))
    elif self.url_pattern == OneJob.DITIEFANG:
      if index == 1:
        return self.OnePath(first, index)
      else:
        return self.TwoPath(first, index)
    elif self.url_pattern == OneJob.CS_DISTRICTS:
      if index == 1:
        return self.OnePath(first, index)
      else:
        number = first.count('/')
        if number == 3:
          return self.ThreePath(first, index)
        elif number == 4:
          return self.TwoPath(first, index)


class OneExcelJob:
  def __init__(self, path, head=BEIJIN_HEAD):
    self.jobs = []
    self.head = head
    self.output_path = path

  def Work(self):
    self.workbook = xlwt.Workbook()
    for job in self.jobs:
      self.SolveOneJob(job)
      #break

    if len(self.jobs) > 0:
      self.workbook.save(self.output_path)


  def AddJobs(self, jobs):
    self.jobs.extend(jobs)

  def AddSubwayJobs(self, url):
    jobs = []
    SafeDriverGet(url)
    execute_times(driver, 1)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, from_encoding="utf8")
    try:
      groups = soup.find_all('div', class_='sbw_group')
      for group in groups:
       links = group.find_all('a', class_='sbw_link ')
       for link in links:
         job = OneJob(link.text, self.head, self.head + link.get('href'), OneJob.DITIEFANG)
         jobs.append(job)
    except:
      pass

    self.AddJobs(jobs)



  def AddDistrictsJobs(self, url):
    jobs = []
    SafeDriverGet(url)
    execute_times(driver, 1)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, from_encoding="utf8")
    try:
      groups = soup.find_all('div', class_='sub_sub_nav section_sub_sub_nav')
      for group in groups:
       links = group.find_all('a')
       for link in links:
         job = OneJob(link.text, self.head, self.head + link.get('href'), OneJob.DISTRICTS)
         jobs.append(job)
    except:
      pass

    self.AddJobs(jobs)


  def SolveOneJob(self, job):
    SafeDriverGet(job.url)
    execute_times(driver, 1)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, from_encoding="utf8")
    pages = GetPagesNumber(soup, job.url)

    out = []
    if pages[1] == None:
      print('error happen!!!')
    elif pages[1] > 1:
      for i in range(1, pages[1] + 1):
        url = job.NextPageURL(pages[0], i)
        # 每个url尝试三次
        for i in range(0, 3):
          data = DealOnePage(url)
          if len(data) != 0:
            out.extend(data)
            break
    elif pages[1] == 1:
      # 每个url尝试三次
      for i in range(0, 3):
        data = DealOnePage(job.url)
        if len(data) != 0:
          out.extend(data)
          break
    else:
      pass

    digest = GenDigest(out)
    self.AddExcel(job.title, out, digest)


  def AddExcel(self, title, data, digest):
    if len(data) == 0:
      return

    sheet = self.workbook.add_sheet(title, cell_overwrite_ok=True)

    # 写上字段信息
    # EXCEL_DUMP = [u'标题', u'片区', u'总价', u'面积', u'房型', u'关注人数', u'带看次数', u'发布天数', u'URL', u'基础信息', u'带看信息', u'楼层信息', u'发布时间']
    for field in range(0, len(OneHouse.EXCEL_DUMP)):
      sheet.write(0, field, OneHouse.EXCEL_DUMP[field])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1, len(data) + 1):
      sheet.write(row, 0, u'%s' % data[row - 1].title)
      sheet.write(row, 1, u'%s' % data[row - 1].location)
      sheet.write(row, 2, data[row - 1].total_money)
      sheet.write(row, 3, data[row - 1].square)
      sheet.write(row, 4, u'%s' % data[row - 1].housetype)

      sheet.write(row, 5, data[row - 1].attention_number)
      sheet.write(row, 6, data[row - 1].follow_number)
      sheet.write(row, 7, data[row - 1].release_number)
      sheet.write(row, 8, u'%s' % data[row - 1].url)
      sheet.write(row, 9, u'%s' % data[row - 1].base_info)
      sheet.write(row, 10, u'%s' % data[row - 1].follow_info)
      sheet.write(row, 11, u'%s' % data[row - 1].floor_info)
      sheet.write(row, 12, u'%s' % data[row - 1].release)

    # write digest
    now_row = len(data) + 1 + 5
    for row in range(now_row, len(digest) + now_row):
      sheet.write(row, 0, u'%s' % digest[row - now_row].name)
      if digest[row - now_row].format != None:
        sheet.write(row, 1, digest[row - now_row].format % digest[row - now_row].content)
      else:
        sheet.write(row, 1, digest[row - now_row].content)




class CSExcelJob(OneExcelJob):
  def __init__(self, path, head):
    OneExcelJob.__init__(self, path, head)



  def AddDistrictsJobs(self, url):
    jobs = []
    SafeDriverGet(url)
    execute_times(driver, 1)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, from_encoding="utf8")
    try:
      group = soup.find('div', attrs={"data-role": "ershoufang"})
      div = group.find_all('div')
      if len(div) == 2:
        links = div[1].find_all('a')
        for link in links:
          job = OneJob(link.text, self.head, self.head + link.get('href'), OneJob.DISTRICTS)
          jobs.append(job)

    except Exception, e:
      print(e)
      pass

    self.AddJobs(jobs)



  def AddSubwayJobs(self, url):
    jobs = []
    SafeDriverGet(url)
    execute_times(driver, 1)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, from_encoding="utf8")
    try:
      group = soup.find('div', attrs={"data-role": "ditiefang"})
      div = group.find_all('div')
      if len(div) == 2:
        links = div[1].find_all('a')
        for link in links:
          job = OneJob(link.text, self.head, self.head + link.get('href'), OneJob.DISTRICTS)
          jobs.append(job)
    except:
      pass

    self.AddJobs(jobs)



class XAExcelJob(OneExcelJob):
  def __init__(self, path, head):
    OneExcelJob.__init__(self, path, head)



  def AddDistrictsJobs(self, url):
    jobs = []
    SafeDriverGet(url)
    execute_times(driver, 1)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, from_encoding="utf8")
    try:
      group = soup.find('div', attrs={"data-role": "ershoufang"})
      div = group.find_all('div')
      if len(div) == 2:
        links = div[0].find_all('a')
        for link in links:
          job = OneJob(link.text, self.head, self.head + link.get('href'), OneJob.DISTRICTS)
          jobs.append(job)

    except Exception, e:
      print(e)
      pass

    self.AddJobs(jobs)


def execute_times(driver, times):
  for i in range(times + 1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)



class OneHouse:
  EXCEL_DUMP = [u'标题', u'片区', u'总价', u'面积', u'房型', u'关注人数', u'带看次数', u'发布天数', u'URL', u'基础信息', u'带看信息', u'楼层信息', u'发布时间']
  def __init__(self):
    self.url = None
    self.title = None
    self.price = None
    self.square = None
    self.total_money = None
    self.location = None
    self.housetype = None
    self.community = None
    self.base_info = None
    self.follow_info = None
    self.floor_info = None
    self.release = None

    self.follow_number = None
    self.release_number = None
    self.attention_number = None


  def GenDigest(self):
    try:
      if self.follow_info != None:
        #长沙的数据/两边有空格。。。
        self.follow_info = self.follow_info.replace(' ', '')
        is_second_type = False
        # number = self.follow_info.count('/')
        # if number == 2:
        #   is_second_type = True
        index = self.follow_info.find(u'人关注')
        index2 = self.follow_info.find(u'次带看')
        index3 = self.follow_info.find(u'以前发布')
        if index != -1:
          self.attention_number = float(self.follow_info[:index])
        if index2 != -1:
          #北京 76次 长沙 共76次
          if self.follow_info[index + 4].isdigit():
            self.follow_number = float(self.follow_info[index + 4:index2])
          else:
            is_second_type = True
            self.follow_number = float(self.follow_info[index + 5:index2])
        release = None
        if index3 != -1:
          if is_second_type == False:
            release = self.follow_info[index2 + 3:index3]
          else:
            release = self.follow_info[index2 + 4:index3]
          if release != None:
            index = release.find(u'天')
            if index != -1:
              self.release_number = float(release[:index])
            else:
              index = release.find(u'个月')
              if index != -1:
                self.release_number = float(release[:index]) * 30
        else:
          index = self.follow_info.find(u'一年前')
          if index != -1:
            self.release_number = 365
          else:
            index = self.follow_info.find(u'刚刚发布')
            if index != -1:
              self.release_number = 1


      if self.release_number != None and self.release == None:
        self.release = unicode(self.release_number)

    except Exception, e:
      print('GenDigest error!!!')
      print(e)



  def Dump(self):
    print(u"房屋信息=========")
    print(u'title ' + self.title)
    print(u'总价 '+ str(self.total_money).decode("utf-8"))
    print(u'户型 ' + self.housetype)
    print(u'面积 ' + str(self.square).decode("utf-8"))
    print(u'关注人数 ' + str(self.attention_number))
    print(u'带看次数 ' + str(self.follow_number))
    print(u'发布天数 ' + str(self.release_number))


class OneDigest:
  def __init__(self,n=None,f=None,c=None):
    self.name = n
    self.format = f
    self.content = c



def String2Number(s):
  import re
  return float(re.findall('([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s)[0][0])









def GenDigest(out):
  digest = []

  digest.append(OneDigest(u'采样日期 ', u'%s', TodayString()))
  digest.append(OneDigest(u'总套数 ', None, len(out)))
  average_total_price = OneDigest(u'平均总价')
  average_price = OneDigest(u'平均单价')
  average_square = OneDigest(u'平均面积')
  average_follow = OneDigest(u'平均带看')
  average_attention = OneDigest(u'平均关注')
  average_release = OneDigest(u'平均发布')

  digest.append(average_total_price)
  digest.append(average_square)
  digest.append(average_price)
  digest.append(average_follow)
  digest.append(average_attention)
  digest.append(average_release)

  if digest[1].content == 0:
    average_total_price.content = 0
    average_square.content = 0
    average_price.content = 0
    average_follow.content = 0
    average_attention.content = 0
    average_release.content = 0
    return digest



  total_price = 0.0
  square = 0.0
  follow = 0.0
  attention = 0.0
  release = 0.0

  for one in out:
    total_price += one.total_money
    square += one.square
    follow += one.follow_number
    attention += one.attention_number
    release += one.release_number

  average_total_price.content = total_price / len(out)
  average_square.content = square / len(out)
  average_price.content = average_total_price.content / average_square.content
  average_follow.content = follow / len(out)
  average_attention.content = attention / len(out)
  average_release.content = release / len(out)

  # digest.append(average_total_price)
  # digest.append(average_square)
  # digest.append(average_price)
  # digest.append(average_follow)
  # digest.append(average_attention)
  # digest.append(average_release)

  return digest



def SafeDriverGet(url):
  for i in range(0, 3):
    try:
      driver.get(url)
      break
    except Exception, e:
      global driver
      print('SafeDriverGet exception happen!!!')
      driver = webdriver.Chrome(CHROME_DRIVER_PATH)
      print(e)

def DealOnePage(url):
  out = []
  #driver = webdriver.Chrome(CHROME_DRIVER_PATH)
  SafeDriverGet(url)
  execute_times(driver, 1)
  html = driver.page_source
  #print(html)
  soup = bs4.BeautifulSoup(html, from_encoding="utf8")
  try:
    table = soup.find('ul', class_='sellListContent')
    all_li = table.find_all('li')
    for li in all_li:
      one_house = OneHouse()
      info = li.find('div', class_='info clear')
      title = info.find('div', class_='title')
      title2 = title.find('a')
      one_house.title = title2.string
      one_house.url = title2.get('href')
      addr = li.find('div', class_='address')
      addr2 = addr.find('div', class_='houseInfo')
      loc = addr2.find('a')
      one_house.location = loc.string
      one_house.base_info = addr2.text
      info_list = one_house.base_info.split(u'/')
      print(one_house.base_info)
      #长沙的info_list 用的|分隔
      if len(info_list) == 1:
        one_house.base_info = one_house.base_info.replace(' ', '')
        info_list = one_house.base_info.split(u'|')
      for i in range(0, len(info_list)):
        if i == 1:
          one_house.community = info_list[i - 1]
        elif i == 2:
          one_house.housetype = info_list[i - 1]
        elif i == 3:
          one_house.square = String2Number(info_list[i - 1])
          break

      floor = info.find('div', class_='flood')
      one_house.floor_info = floor.text
      follow = info.find('div', class_='followInfo')
      one_house.follow_info = follow.text
      price = follow.find('div', class_='priceInfo')
      #cs的price不在follow里面,而是同级别
      if price == None:
        price = info.find('div', class_='priceInfo')

      total_price = price.find('div', class_='totalPrice')
      one_house.total_money = String2Number(total_price.text)
      unit_price = price.find('div', class_='unitPrice')
      one_house.price = unit_price.text
      release = follow.find('div', class_='timeInfo')
      #cs没有发布时间
      if release != None:
        one_house.release = release.text
      one_house.GenDigest()
      one_house.Dump()
      out.append(one_house)

  except Exception, e:
    print('error happen!!!!')
    print(e)
    print(url)
  return out





def GetPagesNumber(soup, url):
  first_url = None
  last_text = None
  number = 0
  page_colunm = soup.find('div', class_='page-box house-lst-page-box')
  if page_colunm != None:
    all_a = page_colunm.find_all('a')

    #只有一页
    if len(all_a) == 0:
      return (None, 1)

    first_url = None
    last_text = None
    for a in all_a:
      href = a.get('href')
      text = a.string
      print(href)
      print(text)
      if text == '1':
        first_url = href
        last_text = text
      elif text == U'下一页':
        number = int(last_text)
        print('max page number' + last_text)
        return (first_url, number)
      else:
        last_text = text

    else:
      #没有下一页
      if first_url != None and last_text != None:
        return (first_url, int(last_text))

  else:
    noresult = soup.find('div', class_='m-noresult')
    if noresult != None:
      print('no result!!!')
      print(url)
      return (None, 0)

  return (None, None)




def WriteExcel(title, data, digest, outpath):
  workbook = xlwt.Workbook()
  sheet = workbook.add_sheet(title, cell_overwrite_ok=True)

  # 写上字段信息
  #EXCEL_DUMP = [u'标题', u'片区', u'总价', u'面积', u'房型', u'关注人数', u'带看次数', u'发布天数', u'URL', u'基础信息', u'带看信息', u'楼层信息', u'发布时间']
  for field in range(0, len(OneHouse.EXCEL_DUMP)):
    sheet.write(0, field, OneHouse.EXCEL_DUMP[field])

  # 获取并写入数据段信息
  row = 1
  col = 0
  for row in range(1, len(data) + 1):
    sheet.write(row, 0, u'%s' % data[row - 1].title)
    sheet.write(row, 1, u'%s' % data[row - 1].location)
    sheet.write(row, 2, data[row - 1].total_money)
    sheet.write(row, 3, data[row - 1].square)
    sheet.write(row, 4, u'%s' % data[row - 1].housetype)

    sheet.write(row, 5, data[row - 1].attention_number)
    sheet.write(row, 6, data[row - 1].follow_number)
    sheet.write(row, 7, data[row - 1].release_number)
    sheet.write(row, 8, u'%s' % data[row - 1].url)
    sheet.write(row, 9, u'%s' % data[row - 1].base_info)
    sheet.write(row, 10, u'%s' % data[row - 1].follow_info)
    sheet.write(row, 11, u'%s' % data[row - 1].floor_info)
    sheet.write(row, 12, u'%s' % data[row - 1].release)


  #write digest
  now_row = len(data) + 1 + 5
  for row in range(now_row, len(digest) + now_row):
    sheet.write(row, 0, u'%s' % digest[row - now_row].name)
    if digest[row - now_row].format != None:
      sheet.write(row, 1, digest[row - now_row].format % digest[row - now_row].content)
    else:
      sheet.write(row, 1, digest[row - now_row].content)

  workbook.save(outpath)



def YJTask():
  # 五号线，按每站
  excel_job = OneExcelJob('C:/workspace/subway5')
  excel_job.AddSubwayJobs('https://bj.lianjia.com/ditiefang/li649s20598/cdo52hu1hy1ba57ea70ep480/')
  excel_job.Work()

  # 八号线，按每站
  excel_job = OneExcelJob('C:/workspace/subway8')
  excel_job.AddSubwayJobs('https://bj.lianjia.com/ditiefang/li659s43145628/cdo52hu1hy1ba57ea70ep480/')
  excel_job.Work()

  # 13号线，按每站
  excel_job = OneExcelJob('C:/workspace/subway13')
  excel_job.AddSubwayJobs('https://bj.lianjia.com/ditiefang/li652s43143244/cdo52hu1hy1ba57ea70ep480/')
  excel_job.Work()

  # 14号线，按每站
  excel_job = OneExcelJob('C:/workspace/subway14')
  excel_job.AddSubwayJobs('https://bj.lianjia.com/ditiefang/li46461179s46107208/cdo52hu1hy1ba57ea70ep480/')
  excel_job.Work()

  # chaoyang
  excel_job = OneExcelJob('C:/workspace/chaoyang')
  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/chaoyang/co52hu1hy1ba57ea70ep480/')
  excel_job.Work()

  # haidian
  excel_job = OneExcelJob('C:/workspace/haidian')
  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/haidian/co52hu1hy1ba57ea70ep480/')
  excel_job.Work()

  pass


def MyTask():
  # 五号线，按每站
  excel_job = OneExcelJob('C:/workspace/mysubway5.xls')
  title = u'5号线'
  url = 'https://bj.lianjia.com/ditiefang/li649/cdo52hu1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DITIEFANG)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddSubwayJobs('https://bj.lianjia.com/ditiefang/li649/cdo52hu1ea20000ep500/')
  excel_job.Work()

  # 八号线，按每站
  excel_job = OneExcelJob('C:/workspace/mysubway8.xls')
  title = u'8号线'
  url = 'https://bj.lianjia.com/ditiefang/li659/cdo52hu1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DITIEFANG)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddSubwayJobs('https://bj.lianjia.com/ditiefang/li659/cdo52hu1ea20000ep500/')
  excel_job.Work()

  # 13号线，按每站
  excel_job = OneExcelJob('C:/workspace/mysubway13.xls')
  title = u'13号线'
  url = 'https://bj.lianjia.com/ditiefang/li652/cdo52hu1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DITIEFANG)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddSubwayJobs('https://bj.lianjia.com/ditiefang/li652/cdo52hu1ea20000ep500/')
  excel_job.Work()

  # 14号线，按每站
  excel_job = OneExcelJob('C:/workspace/mysubway14.xls')
  title = u'14号线'
  url = 'https://bj.lianjia.com/ditiefang/li46461179/cdo52hu1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DITIEFANG)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddSubwayJobs('https://bj.lianjia.com/ditiefang/li46461179/cdo52hu1ea20000ep500/')
  excel_job.Work()

  # chaoyang#############################################################################################
  excel_job = OneExcelJob('C:/workspace/mychaoyang.xls')
  title = u'朝阳区'
  url = 'https://bj.lianjia.com/ershoufang/chaoyang/co52hu1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)


  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/chaoyang/co52hu1ea20000ep500/')
  excel_job.Work()

  # haidian############################################################################################
  excel_job = OneExcelJob('C:/workspace/myhaidian.xls')
  title = u'海淀区'
  url = 'https://bj.lianjia.com/ershoufang/haidian/co52hu1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)


  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/haidian/co52hu1ea20000ep500/')
  excel_job.Work()

  pass


def CSTask():


  # 雨花区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/cs/yuhua.xls', CS_HEAD)
  title = u'雨花区'
  url = 'https://cs.lianjia.com/ershoufang/yuhua/co52/'
  job = OneJob(title, CS_HEAD, url, OneJob.CS_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)


  excel_job.AddDistrictsJobs('https://cs.lianjia.com/ershoufang/yuhua/co52/')
  excel_job.Work()

  # 岳麓区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/cs/yuelu.xls', CS_HEAD)
  title = u'岳麓区'
  url = 'https://cs.lianjia.com/ershoufang/yuelu/co52/'
  job = OneJob(title, CS_HEAD, url, OneJob.CS_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://cs.lianjia.com/ershoufang/yuelu/co52/')
  excel_job.Work()
  #
  # # 天心区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/cs/tianxin.xls', CS_HEAD)
  title = u'天心区'
  url = 'https://cs.lianjia.com/ershoufang/tianxin/co52/'
  job = OneJob(title, CS_HEAD, url, OneJob.CS_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://cs.lianjia.com/ershoufang/tianxin/co52/')
  excel_job.Work()
  #
  # # 开福区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/cs/kaifu.xls', CS_HEAD)
  title = u'开福区'
  url = 'https://cs.lianjia.com/ershoufang/kaifu/co52/'
  job = OneJob(title, CS_HEAD, url, OneJob.CS_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://cs.lianjia.com/ershoufang/kaifu/co52/')
  excel_job.Work()

  # 芙蓉区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/cs/furong.xls', CS_HEAD)
  title = u'芙蓉区'
  url = 'https://cs.lianjia.com/ershoufang/furong/co52/'
  job = OneJob(title, CS_HEAD, url, OneJob.CS_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://cs.lianjia.com/ershoufang/furong/co52/')
  excel_job.Work()

  # 一号线#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/cs/subway1.xls', CS_HEAD)
  # title = u'一号线'
  # url = 'https://cs.lianjia.com/ditiefang/li3511589689553419/'
  # job = OneJob(title, CS_HEAD, url, OneJob.CS_DITIEFANG)
  # jobs = []
  # jobs.append(job)
  # # excel_job.AddJobs(jobs)
  #
  # excel_job.AddSubwayJobs('https://cs.lianjia.com/ditiefang/li3511589689553419/')
  # excel_job.Work()


def BJTask():

  # 东城############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/dongcheng.xls')
  title = u'东城区'
  url = 'https://bj.lianjia.com/ershoufang/dongcheng/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/dongcheng/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 西城############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/xicheng.xls')
  title = u'西城区'
  url = 'https://bj.lianjia.com/ershoufang/xicheng/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/xicheng/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 朝阳############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/chaoyang.xls')
  title = u'朝阳区'
  url = 'https://bj.lianjia.com/ershoufang/chaoyang/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/chaoyang/co52hu1nb1ea20000ep500/')
  excel_job.Work()


  # 海淀############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/haidian.xls')
  title = u'海淀区'
  url = 'https://bj.lianjia.com/ershoufang/haidian/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/haidian/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 丰台############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/fengtai.xls')
  title = u'丰台区'
  url = 'https://bj.lianjia.com/ershoufang/fengtai/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/fengtai/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 石景山############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/sjs.xls')
  title = u'石景山区'
  url = 'https://bj.lianjia.com/ershoufang/shijingshan/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/shijingshan/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 通州############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/tongzhou.xls')
  title = u'通州'
  url = 'https://bj.lianjia.com/ershoufang/tongzhou/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/tongzhou/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  #昌平############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/changping.xls')
  title = u'昌平'
  url = 'https://bj.lianjia.com/ershoufang/changping/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/changping/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 大兴############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/daxing.xls')
  title = u'大兴'
  url = 'https://bj.lianjia.com/ershoufang/daxing/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/daxing/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  #亦庄############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/yizhuang.xls')
  title = u'亦庄开发区'
  url = 'https://bj.lianjia.com/ershoufang/yizhuangkaifaqu/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/yizhuangkaifaqu/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 顺义############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/shunyi.xls')
  title = u'顺义'
  url = 'https://bj.lianjia.com/ershoufang/shunyi/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/shunyi/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 房山############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/fangshan.xls')
  title = u'房山'
  url = 'https://bj.lianjia.com/ershoufang/fangshan/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/fangshan/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 门头沟############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/mentougou.xls')
  title = u'门头沟'
  url = 'https://bj.lianjia.com/ershoufang/mentougou/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/mentougou/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 平谷############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/pinggu.xls')
  title = u'平谷'
  url = 'https://bj.lianjia.com/ershoufang/pinggu/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/pinggu/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 怀柔############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/huairou.xls')
  title = u'怀柔-整体'
  url = 'https://bj.lianjia.com/ershoufang/huairou/co52hu1nb1ea20000ep500/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://bj.lianjia.com/ershoufang/huairou/co52hu1nb1ea20000ep500/')
  excel_job.Work()

  # 燕郊############################################################################################
  excel_job = OneExcelJob('C:/workspace/house/bj/yanjiao.xls')
  title = u'燕郊'
  url = 'https://lf.lianjia.com/ershoufang/yanjiao/co52hu1nb1p1p3p5p6p2p7/'
  job = OneJob(title, BEIJIN_HEAD, url, OneJob.DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://lf.lianjia.com/ershoufang/yanjiao/co52hu1nb1p1p3p5p6p2p7/')
  excel_job.Work()



def XATask():
  'https://xa.lianjia.com/ershoufang/beilin/'
  # 西安区#############################################################################################
  excel_job = XAExcelJob('C:/workspace/house/xa/XA.xls', XA_HEAD)
  excel_job.AddDistrictsJobs('https://xa.lianjia.com/ershoufang/beilin/')
  excel_job.Work()


def SZTask():

  # 罗湖区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/sz/luohu.xls', SZ_HEAD)
  title = u'罗湖区'
  url = 'https://sz.lianjia.com/ershoufang/luohuqu/co52p1p2p3p4/'
  job = OneJob(title, SZ_HEAD, url, OneJob.SZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)


  excel_job.AddDistrictsJobs('https://sz.lianjia.com/ershoufang/luohuqu/co52p1p2p3p4/')
  excel_job.Work()

  # 福田区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/sz/futian.xls', SZ_HEAD)
  title = u'福田区'
  url = 'https://sz.lianjia.com/ershoufang/futianqu/co52p1p2p3p4/'
  job = OneJob(title, SZ_HEAD, url, OneJob.SZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://sz.lianjia.com/ershoufang/futianqu/co52p1p2p3p4/')
  excel_job.Work()

  # 南山区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/sz/nanshan.xls', SZ_HEAD)
  title = u'南山区'
  url = 'https://sz.lianjia.com/ershoufang/nanshanqu/co52p1p2p3p4/'
  job = OneJob(title, SZ_HEAD, url, OneJob.SZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://sz.lianjia.com/ershoufang/nanshanqu/co52p1p2p3p4/')
  excel_job.Work()

  # 盐田区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/sz/yantian.xls', SZ_HEAD)
  title = u'盐田区'
  url = 'https://sz.lianjia.com/ershoufang/yantianqu/co52p1p2p3p4/'
  job = OneJob(title, SZ_HEAD, url, OneJob.SZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://sz.lianjia.com/ershoufang/yantianqu/co52p1p2p3p4/')
  excel_job.Work()

  # 宝安区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/sz/baoan.xls', SZ_HEAD)
  title = u'宝安区'
  url = 'https://sz.lianjia.com/ershoufang/baoanqu/co52p1p2p3p4/'
  job = OneJob(title, SZ_HEAD, url, OneJob.SZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://sz.lianjia.com/ershoufang/baoanqu/co52p1p2p3p4/')
  excel_job.Work()

  # 龙岗区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/sz/longgang.xls', SZ_HEAD)
  title = u'龙岗区'
  url = 'https://sz.lianjia.com/ershoufang/longgangqu/co52p1p2p3p4/'
  job = OneJob(title, SZ_HEAD, url, OneJob.SZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://sz.lianjia.com/ershoufang/longgangqu/co52p1p2p3p4/')
  excel_job.Work()

  # 龙华区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/sz/longhua.xls', SZ_HEAD)
  title = u'龙华区'
  url = 'https://sz.lianjia.com/ershoufang/longhuaqu/co52p1p2p3p4/'
  job = OneJob(title, SZ_HEAD, url, OneJob.SZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://sz.lianjia.com/ershoufang/longhuaqu/co52p1p2p3p4/')
  excel_job.Work()

  # 光明区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/sz/guangming.xls', SZ_HEAD)
  title = u'光明区'
  url = 'https://sz.lianjia.com/ershoufang/guangmingxinqu/co52p1p2p3p4/'
  job = OneJob(title, SZ_HEAD, url, OneJob.SZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://sz.lianjia.com/ershoufang/guangmingxinqu/co52p1p2p3p4/')
  excel_job.Work()

  # 平山区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/sz/pingshan.xls', SZ_HEAD)
  title = u'坪山区'
  url = 'https://sz.lianjia.com/ershoufang/pingshanqu/co52p1p2p3p4/'
  job = OneJob(title, SZ_HEAD, url, OneJob.SZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://sz.lianjia.com/ershoufang/pingshanqu/co52p1p2p3p4/')
  excel_job.Work()

  # 大鹏区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/sz/dapeng.xls', SZ_HEAD)
  title = u'大鹏区'
  url = 'https://sz.lianjia.com/ershoufang/dapengxinqu/co52p1p2p3p4/'
  job = OneJob(title, SZ_HEAD, url, OneJob.SZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddDistrictsJobs('https://sz.lianjia.com/ershoufang/dapengxinqu/co52p1p2p3p4/')
  excel_job.Work()




def HZTask():

  # 滨江区#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/hz/binjiang.xls', HZ_HEAD)
  title = u'滨江区'
  url = 'https://hz.lianjia.com/ershoufang/binjiang/co52p2p3p4p5rs1%E5%8F%B7%E7%BA%BF/'
  job = OneJob(title, HZ_HEAD, url, OneJob.HZ_DISTRICTS)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)


  excel_job.AddDistrictsJobs('https://hz.lianjia.com/ershoufang/binjiang/co52p2p3p4p5rs1%E5%8F%B7%E7%BA%BF/')
  excel_job.Work()



  # 一号线#############################################################################################
  excel_job = CSExcelJob('C:/workspace/house/hz/subway1.xls', HZ_HEAD)
  title = u'一号线'
  url = 'https://hz.lianjia.com/ditiefang/li110460707co52p2p3p4p5rs1%E5%8F%B7%E7%BA%BF/'
  job = OneJob(title, HZ_HEAD, url, OneJob.HZ_DITIEFANG)
  jobs = []
  jobs.append(job)
  excel_job.AddJobs(jobs)

  excel_job.AddSubwayJobs('https://hz.lianjia.com/ditiefang/li110460707co52p2p3p4p5rs1%E5%8F%B7%E7%BA%BF/')
  excel_job.Work()

# =======================================================
if __name__ == '__main__':
  #SZTask()
  #BJTask()
  # HZTask()
  # SZTask()
  # XATask()
  CSTask()
  # MyTask()
  #YJTask()
  #Main()
  #ProvinceDoc()
  # GobalDoc()
  # OneList()

  """
  one = GetChildrenByIndex(table, 'tbody 5 level', 9)
  DealOne(one)
  #print(one)
  #print(dir(one))
  #13 ok
  print('########################################################################')
  one = GetChildrenByIndex(table, 'tbody 5 level', 13)
  print(one)
  DealOne(one)

  """






