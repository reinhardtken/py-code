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
  
  
class HS300:
  KEY_NAME = {
    'code': '股票代码',
    'name': '股票名称',
    'date': '日期',
    'weight': '权重',
  }
  DB_NAME = 'stock'
  COLLECTION_NAME = 'hs300_stock_list'
  