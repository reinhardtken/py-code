import numpy as np
import pandas as pd
import setting
import query.query_yjbg
import query.query_zcfz
import query.query_lrb
import query.query_xjll
import query.query_extra
import query.query_yysj

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
    data_extra = query.query_extra.QueryTop(0, s)
    data_yysj = query.query_yysj.QueryTop(0, s)
    print(data_yysj)
    select_yjbg = data_yjbg[["代码", "名称", "净资产收益率", "销售毛利率",
                   "销售净利率"]]
    select_zcfz = data_zcfz[['资产负债率', '应收账款增长率',
                             '存货增长率']]
    select_lrb = data_lrb[['归属母公司股东的净利润同比增长率(扣除非经常性损益)',
                           '营业收入增长率']]
    select_extra = data_extra[['季度',
                               '应收账款增长率/收入增长率',
                               '存货增长率/收入增长率',
                               '经营活动产生的现金流量净额/营业收入',
                               '每股经营现金流量']]
    if data_yysj['三次变更日期'] is not "-":
        select_yysj = data_yysj['三次变更日期']
    elif data_yysj['二次变更日期'] is not "-":
        select_yysj = data_yysj['二次变更日期']
    elif data_yysj['一次变更日期'] is not "-":
        select_yysj = data_yysj['一次变更日期']
    else:
        select_yysj = data_yysj['首次预约时间']
    select = pd.merge(select_yjbg, select_zcfz, on='季度')
    select = pd.merge(select, select_lrb , on='季度')
    select = pd.merge(select, select_extra, on='季度')
    select = pd.merge(select, select_yysj, on='季度')
    if len(out.index) == 0:
        out = select
    else:
        out = out.append(select)
print(out)
df = pd.DataFrame(out)
df.to_excel(setting.PATH + 'F_data_portfolio.xlsx')
