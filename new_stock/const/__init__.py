#!/usr/bin/env python
# -*- encoding: utf-8 -*-

MONGODB_ID = '_id'
COMMON_ID = '季度'


class CWSJ_KEYWORD:
  ID_NAME = 'date'
  DB_NAME = 'stock'
  COLLECTION_HEAD = 'cwsj-'
  KEY_NAME = {
    "date": "季度",
    "jbmgsy": "基本每股收益(元)",
    "kfmgsy": "扣非每股收益(元)",
    "xsmgsy": "稀释每股收益(元)",
    "mgjzc": "每股净资产(元)",
    "mggjj": "每股公积金(元)",
    "mgwfply": "每股未分配利润(元)",
    "mgjyxjl": "每股经营现金流(元)",
    "yyzsr": "营业总收入(元)",
    "mlr": "毛利润(元)",
    "gsjlr": "归属净利润(元)",
    "kfjlr": "扣非净利润(元)",
    "yyzsrtbzz": "营业总收入同比增长(%)",
    "gsjlrtbzz": "归属净利润同比增长(%)",
    "kfjlrtbzz": "扣非净利润同比增长(%)",
    "yyzsrgdhbzz": "营业总收入滚动环比增长(%)",
    "gsjlrgdhbzz": "归属净利润滚动环比增长(%)",
    "kfjlrgdhbzz": "扣非净利润滚动环比增长(%)",
    "jqjzcsyl": "加权净资产收益率(%)",
    "tbjzcsyl": "摊薄净资产收益率(%)",
    "tbzzcsyl": "摊薄总资产收益率(%)",
    "mll": "毛利率(%)",
    "jll": "净利率(%)",
    "sjsl": "实际税率(%)",
    "yskyysr": "预收款/营业收入",
    "xsxjlyysr": "销售现金流/营业收入",
    "jyxjlyysr": "经营现金流/营业收入",
    "zzczzy": "总资产周转率(次)",
    "yszkzzts": "应收账款周转天数(天)",
    "chzzts": "存货周转天数(天)",
    "zcfzl": "资产负债率(%)",
    "ldzczfz": "流动负债/总负债(%)",
    "ldbl": "流动比率",
    "sdbl": "速动比率",

    'zgb': '总股本',
  }

  DATA_SUB = {}

  NEED_TO_NUMBER = {

    "jbmgsy": "0.2170",
    "kfmgsy": "0.1910",
    "xsmgsy": "0.2170",
    "mgjzc": "2.4372",
    "mggjj": "1.1088",
    "mgwfply": "0.2985",
    "mgjyxjl": "0.7548",
    "yyzsr": "938亿",
    "mlr": "228亿",
    "gsjlr": "75.7亿",
    "kfjlr": "66.8亿",
    "yyzsrtbzz": "36.15",
    "gsjlrtbzz": "301.99",
    "kfjlrtbzz": "53185.01",
    "yyzsrgdhbzz": "1.45",
    "gsjlrgdhbzz": "-7.91",
    "kfjlrgdhbzz": "-13.59",
    "jqjzcsyl": "9.25",
    "tbjzcsyl": "8.92",
    "tbzzcsyl": "3.41",
    "mll": "25.07",
    "jll": "8.38",
    "sjsl": "19.31",
    "yskyysr": "0.01",
    "xsxjlyysr": "1.10",
    "jyxjlyysr": "0.28",
    "zzczzy": "0.41",
    "yszkzzts": "60.84",
    "chzzts": "43.00",
    "zcfzl": "59.28",
    "ldzczfz": "32.76",
    "ldbl": "2.01",
    "sdbl": "1.83"
  }

  ADJUST_NAME = {
    '_id': '_id',
    "date": "季度",
    'QuarterProfit': '当季每股收益',
    'QuarterProfitRatio': '较一季度比例',
    'HalfYearProfitRatio': '较上半年比例',
    'ThreeQuarterProfitRatio': '较前三季度比例',

    'ForecastProfit': '预告基本每股收益',
    'ForecastQuarterProfit': '预告季度每股收益',
    'LastYearProfit': '上一年每股收益',
    'ForecastGrowthRate': '预测增长率',
    'ForecastMidGrowthRate': '预测中间增长率',
    'ForecastFinalGrowthRate': '预测最终增长率',
    'ForecastPerShareProfit': '每股收益预测',
    'PEMin': 'PE下限',
    'PEMax': 'PE上限',
    'ValueMin': '估值下限',
    'ValueMax': '估值上限',
    'LastYearROE': '上年净资产收益率(%)',



    #for test,may not be right place
    'zgb': '总股本',
    'forecastl': '预计净利润下限',
    'djmgsy_jy': '当季每股收益-检验',
    'jyjdbl_jy': '较一季度比例-检验',
    'jsbnbl_jy': '较上半年比例-检验',
    'jqsjdbl_jy': '较前三季度比例-检验',

  }




class YJYG_KEYWORD:
  ID_NAME = 'scode'
  DB_NAME = 'stock'
  COLLECTION_HEAD = 'yjyg-'
  KEY_NAME = {
    "date": "季度",
    'scode': '代码',
    'sname': '名称',
    'hymc': '板块',
    'enddate': '截止日期',
    'forecastl': '预计净利润下限',
    'forecastt': '预计净利润上限',
    'increasel': '业绩变动幅度下限',
    'increaset': '业绩变动幅度上限',
    'forecastcontent': '业绩变动',
    'changereasondscrpt': '业绩变动原因',
    'forecasttype': '预告类型',
    'yearearlier': '上年同期净利润',
    'ndate': '公告日期',
    'sclx': '市场',
  }

  NEED_TO_NUMBER = {

    'forecastl': '预计净利润下限',
    'forecastt': '预计净利润上限',
    'increasel': '业绩变动幅度下限',
    'increaset': '业绩变动幅度上限',
    'yearearlier': '上年同期净利润',

  }

  DATA_SUB = {

    'enddate': '截止日期',
    'ndate': '公告日期',
  }


class GPFH_KEYWORD:
  ID_NAME = 'Code'
  DB_NAME = 'stock'
  COLLECTION_HEAD = 'gpfh-'
  KEY_NAME = {
    'Code': '代码',
    'Name': '名称',
    'XJFH': '现金分红',
    'GXL': '股息率',
    'EarningsPerShare': '每股收益(元)',
    'NetAssetsPerShare': '每股净资产(元)',
    'MGGJJ': '每股公积金(元)',
    'MGWFPLY': '每股未分配利润(元)',
    'JLYTBZZ': '净利润同比增长(%)',
    'TotalEquity': '总股本(亿）',
    'YAGGR': '预案公告日',
    'GQDJR': '股权登记日',
    'CQCXR': '除权除息日',
    'ProjectProgress': '方案进度',
    'NoticeDate': '最新公告日期',
    'SZZBL': '送转总比例',
    'SGBL': '送股比例',
    'ZGBL': '转股比例',
    'AllocationPlan': '分配方案',

  }

  NEED_TO_NUMBER = {

    'XJFH': True,
    'GXL': True,
    'EarningsPerShare': True,
    'NetAssetsPerShare': True,
    'MGGJJ': True,
    'MGWFPLY': True,
    'JLYTBZZ': True,
    'TotalEquity': True,
    'SZZBL': True,
    'SGBL': True,
    'ZGBL': True,
  }

  DATA_SUB = {
    'YAGGR': 1,
    'GQDJR': 1,
    'CQCXR': 1,
    'ReportingPeriod': 1,
    'ResultsbyDate': 1,
    'NoticeDate': 1,
  }


class M012_KEYWORD:
  ID_NAME = '_id'
  DB_NAME = 'stock'
  COLLECTION_HEAD = 'macro-'

  KEY = 'abc'
  MX_TYPE = {

    'M0': 11,
    'M1': 10,
    'M2': 9,
  }

  KEY_NAME = {
    '_id': '月份',
    'data': '同比增幅',
  }



STOCK_LIST = {
  '000725',
  "000651",
  "002508",
  "600566",
  "600487",
  "300298",
  "300642",
  "603595",
  "603156",
  "603868",
  "002517",
  "603387",
  "600690",
  "300628",
  "002626",
  "002294",
  "002372",
  "002415",
  "603516",
  "002901",
  "000848",
  "002032",
  "603833",
  "603160",
  "002304",
  "600519",
  "300741",
  "603288",
}



########################################################
if __name__ == '__main__':
  import sys

  print(sys.path)
  sys.path.append('/home/ken/workspace/code/self/github/py-code/new_stock')
  import util
