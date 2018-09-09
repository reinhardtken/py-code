# -*- coding: utf-8 -*-

# sys
import datetime
import re

# thirdpart
import pandas as pd
import pymongo
from pymongo import MongoClient
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, DateFormatter

#this project
import query
import util
import const

def getWeekofYear():
  iso = datetime.datetime.now().isocalendar()
  return int(iso[0]) * 100 + int(iso[1])