import pandas as pd

from engine.IO import *

monthly_ret = get_ret('M', 1)
momentum_12 = {}
for idx, date in enumerate(monthly_ret.index):
    if idx - 11 >= 0:
        cumulated = monthly_ret.iloc[idx - 11: idx].sum()
        momentum_12[date] = cumulated
        print(1)

momentum_12 = pd.DataFrame(momentum_12).T
momentum_12.index.name = 'date'
momentum_12_path = os.path.join(ARR_DATA, 'Ind', 'Monthly', 'momentum_12.csv')
momentum_12.to_csv(momentum_12_path)

pd.read_csv(momentum_12_path, index_col='date')
print(1)
