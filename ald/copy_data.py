# -*- coding: utf-8 -*-
import urllib
import logging
import re
import datetime

import pymongo
from pymongo import MongoClient

import items
import util
from spiders import toplist_dict


def Copy():
  client = MongoClient()
  db = client["ald"]
  data = toplist_dict.GetList()
  
  for one in data:
    collection = db[one['key']]
    cursor = collection.find()
    for c in cursor:
      # 把其他信息写到db中
      one = {}
      one["_id"] = c["id"]
      one["appkey"] = c["appkey"]
      one["name"] = c["name"]
      one["category"] = c["category"]
      # one["desc"] = c["desc"]
      print("save data {} ".format(one["name"]))
      util.saveMongoDB2(one, "ald", "detail")
      
      
      
if __name__ == '__main__':
  Copy()