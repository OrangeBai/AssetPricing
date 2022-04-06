from engine.allocation import *
from engine.basic import *
from engine.IO import *
from engine.regression import *

## load basic features
rf = risk_free('Daily')
rm = market_return_daily(5, 2, 1)

# get year tags
tags = get_month_splits()
periods = tags_to_periods(tags)

# get features
BE_path = os.path.join(ARR_DATA, 'Ind', 'Daily', 'BE.csv')
MV_path = os.path.join(ARR_DATA, 'Ret', 'Daily', 'Dsmvtll.csv')

BE = pd.read_csv(BE_path, index_col='TradingDate')
MV = pd.read_csv(MV_path, index_col='Trddt')

# construct portfolios
feature_dfs = [MV, BE]
features = [[get_nearest_feature(feature, period[0], period[1]) for feature in feature_dfs] for period in periods]
allocation = allocate_mixed(periods, features, [(0, 0.5, 1), (0, 0.3, 0.7, 1)], ['MV', 'BE'])

data = period_panel(allocation)
HML = cal_feature(data, ['MV0BE2', 'MV1BE2'], ['MV0BE0', 'MV1BE0'])
SMB = cal_feature(data, ['MV0BE1', 'MV0BE1', 'MV0BE2'], ['MV1BE1', 'MV1BE1', 'MV1BE2'])
MKT = market_return_daily(5, 2, 1)

ret = get_ret(1)

factors = pd.DataFrame(data={'MKT': MKT, 'HML': HML, 'SMB': SMB})

trading_dates = MKT.index
selected_dates = get_trade_dates('2000-01-01', '2022-01-01')

start = '2000-01-01'
end = '2022-01-01'
alpha = dict.fromkeys(trading_dates)
beta = dict.fromkeys(trading_dates)
res = dict.fromkeys(trading_dates)
for idx, date in enumerate(trading_dates):
    t = time.time()
    if start <= date < end:
        idx_start = idx - 30
        reg_dates = trading_dates[idx_start: idx + 1]
        reg_target = select_portfolio(ret, (reg_dates[0], reg_dates[-1]))
        cur_reg = reg_target.loc[:, reg_target.isna().sum(axis=0) < 3]
        cur_fac = factors.loc[cur_reg.index, :]

        beta_cur = dict.fromkeys(list(cur_reg.columns))
        res_cur = dict.fromkeys(list(cur_reg.columns))
        alpha_cur = dict.fromkeys(list(cur_reg.columns))

        for StkId, stock in cur_reg.iteritems():
            res = regression(stock, cur_fac)
            res_cur[StkId] = res.resid
            beta_cur[StkId] = res.params['MKT']
            alpha_cur[StkId] = res.params['const']
        print('Date: {0}, num: {1}, time: {2:.4f}'.format(date, cur_reg.shape[1], time.time() - t))
        alpha[date] = alpha_cur
        beta[date] = beta_cur
        res_cur[date] = res_cur

print(1)
