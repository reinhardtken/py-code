import query.query_yjbg

code = '000636'
out = query.query_yjbg.QueryTop(3, code)
print(out['销售毛利率'])