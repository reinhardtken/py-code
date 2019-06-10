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

def run():
    stock_list = setting.f_data_stocklist()
    out = pd.DataFrame()
    out_remix = pd.DataFrame()
    forecast_date = pd.DataFrame()
    forecast_date_remix = pd.DataFrame()
    for s in stock_list:
        data_yjbg = query.query_yjbg.QueryTop(0, s)
        data_zcfz = query.query_zcfz.QueryTop(0, s)
        data_lrb = query.query_lrb.QueryTop(0, s)
        data_extra = query.query_extra.QueryTop(0, s)
        data_yysj = query.query_yysj.QueryTop(0, s)

        print(data_yysj)

        select_yjbg = data_yjbg[["代码", "名称", "_id", "净资产收益率",
                                     "销售毛利率", "销售净利率", "assigndscrpt"]]
        if '应收账款增长率'in data_zcfz and '存货增长率' in data_zcfz:
            select_zcfz = data_zcfz[['_id', '资产负债率', '应收账款增长率',
                                 '存货增长率']]
        if '应收账款/总资产' in data_zcfz:
            select_zcfz['应收账款/总资产'] = data_zcfz['应收账款/总资产']
        if '存货/总资产' in data_zcfz:
            select_zcfz['存货/总资产'] = data_zcfz['存货/总资产']
        select_lrb = data_lrb[['_id',
                        '归属母公司股东的净利润同比增长率(扣除非经常性损益)',
                        '营业收入增长率']]
        if '应收账款增长率/收入增长率' in data_extra and \
            '存货增长率/收入增长率' in data_extra and \
            '经营活动产生的现金流量净额/营业收入' in data_extra and \
            '每股经营现金流量' in data_extra:
            select_extra = data_extra[['_id', '应收账款增长率/收入增长率',
                                   '存货增长率/收入增长率',
                                   '经营活动产生的现金流量净额/营业收入',
                                   '每股经营现金流量']]
        select = pd.merge(select_yjbg, select_zcfz, on='_id')
        select = pd.merge(select, select_lrb , on='_id')
        select = pd.merge(select, select_extra, on='_id')
        select = pd.merge(select, data_yysj, on='_id')
        data_yysj['代码'] = data_yjbg['代码']
        data_yysj['名称'] = data_yjbg['名称']
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
    out_remix['预约披露时间'] = out['首次预约时间']
    out_remix['利润分配'] = out['assigndscrpt']
    df = pd.DataFrame(out_remix)
    df.to_excel(setting.PATH + 'F_data_' + setting.F_data_stock_list_name +
                '.xlsx', index=False)

    forecast_date_remix['代码'] = forecast_date['代码']
    forecast_date_remix['名称'] = forecast_date['名称']
    forecast_date_remix['报告期'] = forecast_date['_id']
    forecast_date_remix['首次预约时间'] = forecast_date['首次预约时间']
    forecast_date_remix['一次变更日期'] = forecast_date['一次变更日期']
    forecast_date_remix['二次变更日期'] = forecast_date['二次变更日期']
    forecast_date_remix['三次变更日期'] = forecast_date['三次变更日期']
    forecast_date_remix.to_excel(setting.PATH + 'forecast_date_' +
            setting.F_data_stock_list_name + '.xlsx', index=False)

if __name__ == '__main__':
    run()