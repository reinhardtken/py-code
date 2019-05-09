import numpy as np
import pandas as pd
import setting
import query.query_yjbg
import query.query_zcfz
import query.query_lrb
import query.query_xjll
import query.query_extra
import query.query_yysj
import query.query_stock_list

date_input = '2018-12-31'
def run(date_input):
    date = date_input
    stock_list = setting.f_data_stocklist()
    out = pd.DataFrame()
    out_remix = pd.DataFrame()
    forecast_date = pd.DataFrame()
    for s in stock_list:
        data_yjbg = query.query_yjbg.QueryTop(100, s)
        data_zcfz = query.query_zcfz.QueryTop(100, s)
        data_lrb = query.query_lrb.QueryTop(100, s)
        data_extra = query.query_extra.QueryTop(100, s)
        data_yysj = query.query_yysj.QueryTop(100, s)
        list = query.query_stock_list.queryOne(s)
        data_yysj['代码'] = s
        data_yysj['名称'] = list['名称']

        print(data_yysj)
        select_yjbg = data_yjbg.loc[data_yjbg['_id'] == date,
                                    ["代码", "名称", "_id", "净资产收益率",
                                     "销售毛利率", "销售净利率"]]
        select_zcfz = data_zcfz.loc[data_zcfz['_id'] == date, ['_id',
                                    '资产负债率', '应收账款增长率', '存货增长率']]
        if '应收账款/总资产' in data_zcfz:
            select_zcfz['应收账款/总资产'] = data_zcfz.loc[data_zcfz['_id'] == date,
                                    '应收账款/总资产']
        if '存货/总资产' in data_zcfz:
            select_zcfz['存货/总资产'] = data_zcfz.loc[data_zcfz['_id'] == date,
                                    '存货/总资产']
        select_lrb = data_lrb.loc[data_lrb['_id'] == date, ['_id',
                               '归属母公司股东的净利润同比增长率(扣除非经常性损益)',
                               '营业收入增长率']]
        select_extra = data_extra.loc[data_extra['_id'] == date,
                                    ['_id', '应收账款增长率/收入增长率',
                                   '存货增长率/收入增长率',
                                   '经营活动产生的现金流量净额/营业收入',
                                   '每股经营现金流量']]
        select = pd.merge(select_yjbg, select_zcfz, on='_id')
        select = pd.merge(select, select_lrb , on='_id')
        select = pd.merge(select, select_extra, on='_id')
        if len(forecast_date.index) == 0:
            forecast_date = data_yysj
        else:
            forecast_date = forecast_date.append(data_yysj)
        if len(out.index) == 0:
            out = select
        else:
            out = out.append(select)
    out_remix["代码"] = out["代码"]
    out_remix["名称"] = out["名称"]
    out_remix['报告期'] = out['_id']
    out_remix['净资产收益率'] = out['净资产收益率']
    out_remix['资产负债率'] = out['资产负债率']
    out_remix['销售毛利率'] = out['销售毛利率']
    out_remix['销售净利率'] = out['销售净利率']
    out_remix['应收账款/总资产'] = out['应收账款/总资产']
    out_remix['存货/总资产'] = out['存货/总资产']
    out_remix['归属母公司股东的净利润同比增长率(扣除非经常性损益)'] = \
        out['归属母公司股东的净利润同比增长率(扣除非经常性损益)']
    out_remix['营业收入增长率'] = out['营业收入增长率']
    out_remix['应收账款增长率'] = out['应收账款增长率']
    out_remix['存货增长率'] = out['存货增长率']
    out_remix['应收账款增长率/收入增长率'] = out['应收账款增长率/收入增长率']
    out_remix['存货增长率/收入增长率'] = out['存货增长率/收入增长率']
    out_remix['经营活动产生的现金流量净额/营业收入'] = \
        out['经营活动产生的现金流量净额/营业收入']
    out_remix['每股经营现金流量'] = out['每股经营现金流量']

    df = pd.DataFrame(out_remix)
    df.to_excel(setting.PATH + date + '_F_data_fixdate.xlsx', index=False)

if __name__ == '__main__':
    run(date_input)