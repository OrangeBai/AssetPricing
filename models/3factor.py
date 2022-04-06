from config import *
from engine.panel import *
from engine.allocation import *
from engine.basic import *

years = get_year_splits()

PB_path = os.path.join(ARR_DATA, 'Ind', 'Daily', 'adjTO.csv')
MV_path = os.path.join(ARR_DATA, 'Ret', 'Daily', 'Dsmvtll.csv')

PB = pd.read_csv(PB_path, index_col='TradingDate')
MV = pd.read_csv(MV_path, index_col='Trddt')

feature_dfs = [MV, PB]
periods = tags_to_periods(years)
features = [[feature.loc[period[0]] for feature in feature_dfs] for period in periods]


allocation = allocate_all_periods(periods, features, [(0, 0.5, 1), (0, 0.3, 0.7, 1)], ['MV', 'PB'])
data = period_panel(allocation)
feature = cal_feature(data, ['MV0PB0', 'MV1PB0'], ['MV0PB2', 'MV1PB2'])

from scipy.stats import ttest_1samp
print(1)
