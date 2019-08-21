#!/usr/bin/env python
# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-

import random


def test():
  STOCK_NUMBER = 100
  TRY_TIMES = 200
  stock = []
  for i in range(STOCK_NUMBER):
    stock.append(random.uniform(100, 1000))
    
  #print(stock)
  #策略A等权重的按初始价格买入每一个股票。之后再也不动
  #策略B以同样的本金每轮随机买入一个股票。
  #每轮，每个股票随机的涨跌
  
  cost = 0
  for i in range(STOCK_NUMBER):
    cost += stock[i]
    
  #print("the total cost {}".format(cost))
  
  #初始条件
  costB = cost
  # chose = random.randint(0, STOCK_NUMBER - 1)
  # numberB = costB / stock[chose]
  accWin = 0
  accLose = 0
  numberWin = 0
  numberLose = 0

  #开始循环
  for i in range(TRY_TIMES):
    #下一次股票的涨跌
    futureStock = []
    winList = []
    loseList = []
    for j in range(STOCK_NUMBER):
      # r = random.uniform(-0.2, 0.3)
      # r = random.uniform(-0.1, 0.15)
      r = random.uniform(-0.05, 0.1)
      #记录所有上涨的id和下跌的id
      if r > 0:
        winList.append(j)
      else:
        loseList.append(j)
      temp = stock[j] * (1 + r)
      futureStock.append(temp)



    #这一次选择
    #作弊
    winLose = random.randint(1, 100)
    newChose = None
    # if winLose > 40:
    #   numberWin += 1
    #   newChose = winList[random.randint(0, len(winList) - 1)]
    # else:
    #   numberLose += 1
    #   newChose = loseList[random.randint(0, len(loseList) - 1)]
    #随机
    newChose = random.randint(0, STOCK_NUMBER - 1)

    # 计算收益
    number = costB / stock[newChose]
    newCostB = number * futureStock[newChose]
    if newCostB > costB:
      numberWin += 1
      accWin += newCostB - costB
    else:
      numberLose += 1
      accLose += costB - newCostB
    costB = newCostB
    stock = futureStock
    
    
    
    

    

  costA = 0
  for i in range(STOCK_NUMBER):
    costA += stock[i]
    
  # print("the  costA {}".format(costA))
  #
  # print("the  costB {}".format(costB))
  print("a, loseb winb final b {}, {}, {}, {}, {}, {}".format(costA, accLose, accWin, costB, numberWin, numberLose))
  
  return costA > costB
  
  
  
if __name__ == '__main__':
  a = 0
  b = 0
  for i in range(500):
    k = test()
    if i % 10 == 0:
      print("i is {}".format(i))
      
    if k:
      a += 1
    else:
      b += 1
      
    
  print("a and b {} {}".format(a, b))