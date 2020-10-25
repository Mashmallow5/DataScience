import pandas as pd
data_xls = pd.read_excel('D:\\out2.xlsx', 'Sheet', index_col=None)
data_xls.to_csv('D:\\out_vih.csv', encoding='utf-8', index = False)
