# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from dateutil import parser
from pytz import timezone
import traceback
from queue import PriorityQueue

# thirdpart
import pandas as pd
from pymongo import MongoClient
import numpy as np

import const
import util

from comm import TradeResult
from comm import TradeMark
from comm import Pump
from comm import Retracement
from comm import MaxRecord
from comm import Priority
from comm import Task


SUGGEST_BUY_EVENT = 11


class FundManager:
  def __init__(self, ):
    self.TOTALMONEY = 500000
    
  def Process(self, context, task):
    if task.key == SUGGEST_BUY_EVENT:
      #无条件转发
      context.AddTask(
        Task(
          Priority(
            4, 2500),
          5, None, *task.args))
      #实际上缓存信号，等到stage完成后，进行资金管理再转发
    
  
  def AfterSellStage(self, stage):
    #在这里做资金管理后再真正转发
    pass