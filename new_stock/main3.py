#!/usr/bin/env python
# -*- encoding: utf-8 -*-

def calc():
  costBase = 12
  costInc = 1.1
  profitBase = 800
  profitInc = 1.05

  costArray = []
  profitArray = []

  currentCost = costBase
  currentProfit = None
  lastProfit = profitBase

  for i in range(30):
    currentProfit = (lastProfit - currentCost) * profitInc
    currentCost = currentCost * costInc

    costArray.append(currentCost)
    profitArray.append(currentProfit)

    lastProfit = currentProfit

  result = []
  for i in range(30):
    result.append([2023+i, costArray[i], profitArray[i]])

  for item in result:
    print("%d %.2f %.2f" % (item[0], item[1], item[2]))



if __name__ == '__main__':
  calc()