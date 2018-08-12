#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class BASICS:
  KEY_NAME = {
    'code': '代码',
    'name': '名称',
    'industry': '所属行业',
    'area': '地区',
    'pe': '市盈率',
    'outstanding': '流通股本(亿)',
    'totals': '总股本(亿)',
    'totalAssets': '总资产(万)',
    'liquidAssets': '流动资产',
    'fixedAssets': '固定资产',
    'reserved': '公积金',
    'reservedPerShare': '每股公积金',
    'esp': '每股收益',
    'bvps': '每股净资',
    'pb': '市净率',
    'timeToMarket': '上市日期',
    'undp': '未分利润',
    'perundp': '每股未分配',
    'rev': '收入同比(%)',
    'profit': '利润同比(%)',
    'gpr': '毛利率(%)',
    'npr': '净利润率(%)',
    'holders': '股东人数',

    #http://www.szse.cn/api/report/index/companyGeneralization?
    #http://query.sse.com.cn/security/stock/queryCompanyStockStruct.do?
    'zgb': '总股本(股)'
  }

  DB_NAME = 'stock'
  COLLECTION_NAME = 'stock_list'



class HS300:
  KEY_NAME = {
    'code': '股票代码',
    'name': '股票名称',
    'date': '日期',
    'weight': '权重',
  }
  DB_NAME = 'stock'
  COLLECTION_NAME = 'hs300_stock_list'



class KData:
  DB_NAME = 'stock_kdata'
  COLLECTION_D_HEAD = ''
  COLLECTION_W_HEAD = 'w_'
  COLLECTION_M_HEAD = 'm_'