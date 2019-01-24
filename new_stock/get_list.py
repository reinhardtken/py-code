import pandas as pd
import setting
import tushare as ts

def get_ts_zz500():
    list = ts.get_zz500s()
    con = list['code'].apply(str)
    return con

def get_ts_cybz():
    list = ts.get_gem_classified()
    con = list['code'].apply(str)
    return con

def get_zz500():
    list = pd.read_excel(setting.list_path + 'zz500.xlsx',
                         converters={u'代码': str}, index_col=False)
    con = list['代码'].apply(str)
    return con

def get_cybz():
    list = pd.read_excel(setting.list_path + 'cybz.xlsx',
                         converters={u'代码': str}, index_col=False)
    con = list['代码'].apply(str)
    return con

def get_all():
    list = pd.read_excel(setting.list_path + 'all.xlsx',
                         converters={u'代码':str}, index_col=False)
    con = list['代码'].apply(str)
    return con

def get_portfolio():
    list = pd.read_excel(setting.list_path + 'portfolio.xlsx',
                         converters={u'代码': str}, index_col=False)
    con = list['代码'].apply(str)
    return con

def get_zxbz():
    list = pd.read_excel(setting.list_path + 'zxbz.xlsx',
                         converters={u'代码': str}, index_col=False)
    con = list['代码'].apply(str)
    return con

if __name__ == '__main__':
    test = get_ts_cybz()
    print(test)