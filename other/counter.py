#!/usr/bin/env python
# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-


import xlwt

import xlrd
import types
import time
import pandas as pd
from selenium import webdriver
import bs4

URL_HEAD = 'http://www.appchina.com/app/'
CHROME_DRIVER_PATH = '/home/ken/prog/chromedriver_linux64/chromedriver'
driver = webdriver.Chrome(CHROME_DRIVER_PATH)



def SafeDriverGet(url):
  for i in range(0, 3):
    try:
      driver.get(url)
      break
    except Exception as e:
      # global driver
      print('SafeDriverGet exception happen!!!')
      # driver = webdriver.Chrome(CHROME_DRIVER_PATH)
      print(e)



def GotoEnd(driver):
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  time.sleep(1)


def pullName(packages):
  nameList = []
  despList = []
  i = 0
  for package in packages:
    # i += 1
    # if i >10:
    #   break
    name = None
    description = None
    try:
      SafeDriverGet(URL_HEAD + package)
      GotoEnd(driver)
      html = driver.page_source
      soup = bs4.BeautifulSoup(html, from_encoding="utf8")

      name = soup.find('h1', class_='app-name')
      if name != None:
        name = name.text

      description = None
      # node = soup.find('h2', class_='part-title')
      # node1 = None
      # node2 = None
      # if node != None:
      #   node1 = node.next_sibling
      #   if node1 != None:
      #     node2 = node1.next_sibling
      #   if node2 != None:
      #     description = node2.text

      node = soup.find('p', class_= 'art-content')
      if node != None:
        description = node.text


      if name != None:
        print(name)
      if description != None:
        print(description)

    except Exception as e:
      print(e)

    nameList.append(name)
    despList.append(description)


  return (nameList, despList)


def test():
  path = '/home/ken/workspace/tmp/launcher.xlsx'
  df = pd.read_excel(path)
  g = df.groupby('dt')
  for k, v in g:
    print(k)
    # print(type(v))
    print(v)
    # print(v.sum())
    sumPV = v.loc[:, ['PV']].sum()
    sumUV = v.loc[:, ['UV']].sum()
    # print(type(sum))
    # print(sum)
    # print(sum['手机数量'])
    totalPV = sumPV['PV']
    totalUV = sumUV['UV']
    # print(total)
    v['percentPV'] = v.apply(lambda x: x['PV'] / totalPV, axis=1)
    v['percentUV'] = v.apply(lambda x: x['UV'] / totalUV, axis=1)
    # print(v)
    # v.sort_values(by=['percent'], ascending=False, inplace=True)
    v.sort_values(by=['PV'], ascending=False, inplace=True)
    v['cumPV'] = v['percentPV'].cumsum()
    v.to_excel('/home/ken/workspace/tmp/launcher-' + str(k) + '-pv.xlsx')

    v.sort_values(by=['UV'], ascending=False, inplace=True)
    v['cumUV'] = v['percentUV'].cumsum()
    v.to_excel('/home/ken/workspace/tmp/launcher-' + str(k) + '-uv.xlsx')
    pass


def test2():
  path = '/home/ken/workspace/tmp/notification.xlsx'
  v = pd.read_excel(path)
  v = v.loc[0:200, :]
  out = pullName(v['应用包名'])
  v['包名'] = out[0]
  v['描述'] = out[1]
  sumPV = v.loc[:, ['PV']].sum()
  sumUV = v.loc[:, ['UV']].sum()
  # print(type(sum))
  # print(sum)
  # print(sum['手机数量'])
  totalPV = sumPV['PV']
  totalUV = sumUV['UV']
  # print(total)
  v['percentPV'] = v.apply(lambda x: x['PV'] / totalPV, axis=1)
  v['percentUV'] = v.apply(lambda x: x['UV'] / totalUV, axis=1)
  # print(v)
  # v.sort_values(by=['percent'], ascending=False, inplace=True)
  v.sort_values(by=['PV'], ascending=False, inplace=True)
  v['cumPV'] = v['percentPV'].cumsum()
  v.to_excel('/home/ken/workspace/tmp/notification-' + '-pv.xlsx')

  v.sort_values(by=['UV'], ascending=False, inplace=True)
  v['cumUV'] = v['percentUV'].cumsum()
  v.to_excel('/home/ken/workspace/tmp/notification-' + '-uv.xlsx')


#################################################################################
if __name__ == '__main__':
  test2()

  pass