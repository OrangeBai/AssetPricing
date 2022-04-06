import os.path
from statsmodels.stats.weightstats import ttest_ind
from scipy.stats import ttest_1samp
import pandas as pd
from config import *
import re
import numpy as np


pattern = re.compile(r'(([a-zA-Z]*)([0-9]*))*')
st = '1998-05'
ed = '2021-11'
path = os.path.join(RES_DIR, 'des', '20')
files = os.listdir(path)

groups = [2, 10]
index = list(range(0, groups[1] + 1)) + ['diff', 't', 'p']

df = pd.DataFrame()
for file in files:
    name, ext = os.path.splitext(file)
    if ext == '.csv':
        temp = pd.read_csv(os.path.join(path, file), index_col=0).loc[st:ed, :]
        for i in range(groups[0]):
            temp_df = temp[[col_name for col_name in temp.columns if 'MV' + str(i) in col_name]]
            diff = temp_df.iloc[:, -1] - temp_df.iloc[:, 0]
            t_res = ttest_1samp(diff, 0)
            res = list(temp_df.mean() * 100) + [diff.mean(), t_res.statistic, t_res.pvalue]
            df[name + 'MV' + str(i)] = pd.Series(res)

df = pd.DataFrame(df)


# def split_df(df, names, groups):
#     path = os.path.join(RES_DIR, 'des', '20')
#     df = pd.read_csv(os.path.join(path, 'NetIssue.csv'), index_col=0)
#     new_df = {}
#     for name in df.columns:
#         pattern = re.compile(r'(([a-zA-Z])*([0-9])*)*')
#         m = re.match(pattern, name)

