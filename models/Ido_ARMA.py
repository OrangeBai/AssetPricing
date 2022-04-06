from engine.allocation import *
from utils.date import *
import time
from scipy.stats import f_oneway

# set up parameters
date_skip = 5
before_dates = 30
after_dates = 60
before_idx = before_dates // date_skip
after_idx = after_dates // date_skip
dates = get_trade_dates(['2000-01-01', '2022-01-01'])
dates = [dates[i] for i in range(0, len(dates), date_skip)]

# load turnover
TO_path = os.path.join(ARR_DATA, 'Ind', 'Daily', 'Turnover.csv')
TO = pd.read_csv(TO_path, index_col=0)

# load adjusted turnover
adjTO_path = os.path.join(ARR_DATA, 'Ind', 'Daily', 'AdjTO.csv')
adjTO = pd.read_csv(adjTO_path, index_col=0)

# load market value
MV_path = os.path.join(ARR_DATA, 'Ret', 'Daily', 'Dsmvtll.csv')
MV = pd.read_csv(MV_path, index_col='Trddt')

feature_dfs = [MV, adjTO]
periods = [(dates[idx - before_idx], dates[idx + after_idx]) for idx in
           range(before_idx, len(dates[before_idx:-after_idx]))]
features = [[feature.loc[date] for feature in feature_dfs] for date in dates[before_idx:-after_idx]]

allocation = allocate_all_periods(periods, features, [(0, 0.5, 1), (0, 0.3, 0.7, 1)], ['MV', 'adjTO'])

mkt_val_all = get_mkt_val(0)
ret_val_all = get_ret(1)

all_p = {}
for name, p in allocation.items():
    t = time.time()
    all_p[name] = []
    for date, portfolios in p:
        all_p[name].append(weighted_return(mkt_val_all, ret_val_all, date, portfolios).reset_index(drop=True))
    all_p[name] = pd.DataFrame(all_p[name])

f_plt = {}
p_plt = {}
for name, df in all_p.items():
    df_list = df.T.values.tolist()
    f_res = []
    p_res = []
    for i in range(0, 85, 1):
        f_res += [[i, f_oneway(*df_list[i: i + 5])[0]]]
        p_res += [[i, f_oneway(*df_list[i: i + 5])[1]]]
    f_plt[name] = np.array(f_res)
    p_plt[name] = np.array(p_res)


from plots.plot_settings import *
c = tableau_color_list()
fig, ax = plt.subplots()

for name, values in p_plt.items():
    ax.plot(values[:, 0], np.log(values[:, 1]))

plt.show()

# ppd = {}
# for n, l in all_p.items():
#     ppd[n] = pd.DataFrame(l).mean(axis=0)
#
# from scipy.stats import f_oneway
#
# f_oneway()
#
# # fpr n, l in ppd.items():
# import statsmodels.api as sm
#
# sm.stats.anova_lm()
# ppd = pd.DataFrame(ppd)
# print(1)

# data = ppd['MV0adjTO0'][25:]
# temp = np.array(data)
# t = adfuller(temp)  # ADF检验
# output = pd.DataFrame(
#     index=['Test Statistic Value', "p-value", "Lags Used", "Number of Observations Used", "Critical Value(1%)",
#            "Critical Value(5%)", "Critical Value(10%)"], columns=['value'])
# output['value']['Test Statistic Value'] = t[0]
# output['value']['p-value'] = t[1]
# output['value']['Lags Used'] = t[2]
# output['value']['Number of Observations Used'] = t[3]
# output['value']['Critical Value(1%)'] = t[4]['1%']
# output['value']['Critical Value(5%)'] = t[4]['5%']
# output['value']['Critical Value(10%)'] = t[4]['10%']
#
# from statsmodels.tsa.stattools import acf, pacf, arma_order_select_ic, diff
#
# lag_acf = acf(data, nlags=20)
# lag_pacf = pacf(data, nlags=20, method='ols')
# od = arma_order_select_ic(data, max_ar=6, max_ma=4, ic='bic')['aic_min_order']
#
# from statsmodels.tsa.arima.model import ARIMA
#
# data = diff(ppd['MV0adjTO0'][25:])
# order = (2, 0, 2)
# tempModel = ARIMA(data, order=order).fit()
#
# delta = tempModel.fittedvalues - data  # 残差
# score = 1 - delta.var() / data.var()
