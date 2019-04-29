import numpy as np
import pandas as pd
import setting
import query.query_yjbg
import query.query_zcfz
import query.query_lrb
import query.query_xjll

code = '000636'
date = '2018-09-30'
stock_list = setting.f_data_stocklist()
select = pd.DataFrame()
out = pd.DataFrame()
for s in stock_list:
    data_yjbg = query.query_yjbg.QueryTop(0, s)
    data_zcfz = query.query_zcfz.QueryTop(0, s)
    data_lrb = query.query_lrb.QueryTop(0, s)
    data_xjll = query.query_lrb.QueryTop(0, s)
    select_yjbg = data_yjbg[['代码', '名称', '_id', '净资产收益率', '销售毛利率',
                   '销售净利率']]
    select_zcfz = data_zcfz[['代码', '资产负债率', '应收账款增长率',
                             '存货增长率']]
    select_lrb = data_lrb[['代码',
                           '归属母公司股东的净利润同比增长率(扣除非经常性损益)',
                           '营业收入增长率']]
    select_xjll = data_xjll[['代码']]
    select = pd.merge(select_yjbg, select_zcfz, on='代码')
    select = pd.merge(select, select_lrb , on='代码')
    if len(out.index) == 0:
        out = select
    else:
        out = out.append(select, ignore_index=True)
print(out)
df = pd.DataFrame(out)
df.to_excel(setting.PATH + 'F_data_portfolio.xlsx', index=False)
