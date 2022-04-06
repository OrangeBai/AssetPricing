import pandas as pd
from config import *
import time

TO_path = os.path.join(ARR_DATA, 'Ind', 'Daily', 'Turnover.csv')
TO = pd.read_csv(TO_path, index_col='TradingDate')
dates_nums = TO.shape[0]

avgTO = TO.mean(axis=1)
# Daily turnover subtract daily average turnover
redTO = TO.subtract(avgTO, axis='index')

# For each trading day T, calculate the average turnover of T-125 to T-5
adjTO = {}
adjTORate = {}
for index_name, row in redTO.iterrows():
    t = time.time()
    idx = redTO.index.get_loc(index_name)
    pre_avg = redTO.iloc[max(0, idx - 120):max(0, idx), :].mean()
    adjTO[index_name] = row.subtract(pre_avg)
    adjTORate[index_name] = row.subtract(pre_avg) / pre_avg
    print(time.time() - t)

adjTOPD = pd.DataFrame(adjTO).T
adjTOPD.index.name = 'TradingDate'

adjTORate = pd.DataFrame(adjTORate).T
adjTORate.index.name = 'TradingDate'

adjTOPD.to_csv(os.path.join(ARR_DATA, 'Ind', 'Daily', 'AdjTO.csv'), encoding='utf-8')
adjTORate.to_csv(os.path.join(ARR_DATA, 'Ind', 'Daily', 'AdjTORate.csv'), encoding='utf-8')

a = pd.DataFrame()
a.to_csv
