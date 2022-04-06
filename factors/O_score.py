import pandas as pd

from engine.IO import *
import numpy as np

total_asset = get_statement_val(ID='A001000000')
total_debt = get_statement_val(ID='A002000000')

current_asset = get_statement_val(ID='A001100000')
current_liability = get_statement_val(ID='A002100000')

net_profit = get_statement_val(ID='B002000000')
operating_income = get_statement_val('B001100000')

stock_ids = intersection(total_asset.columns, net_profit.columns)
stock_ids.sort()
years = get_year_tags()
annual_dates = list(total_asset.index)
quarter_dates = [date for date in list(total_asset.columns) if '-01-01' not in date]

logTA = total_asset.apply(np.log)
TLTA = total_debt / total_asset
WCTA = (current_asset - current_liability) / total_asset
CLCA = current_liability / current_asset

OENEG = pd.DataFrame(columns=current_liability.columns, index=current_liability.index)
OENEG_index = current_liability > current_asset
OENEG[OENEG_index] = 1
OENEG_index = current_liability <= current_asset
OENEG[OENEG_index] = 0
NITA = net_profit / total_asset
FUTL = operating_income / total_debt

INTWO = pd.DataFrame(columns=current_liability.columns, index=current_liability.index)
for idx, date_0 in enumerate(annual_dates[1:]):
    date__1 = annual_dates[idx]
    INTWO_pos = np.all(net_profit.loc[[date__1, date_0], :] < 0, axis=0)
    stk_ids = list(INTWO_pos[INTWO_pos == True].index)
    if len(stk_ids) > 0:
        INTWO.loc[date_0, stk_ids] = 1

    INTWO_neg = np.any(net_profit.loc[[date__1, date_0], :] >= 0, axis=0)
    stk_ids = list(INTWO_neg[INTWO_neg == True].index)
    if len(stk_ids) > 0:
        INTWO.loc[date_0, stk_ids] = 0


CHIN = pd.DataFrame(index=annual_dates, columns=stock_ids)
for idx, date in enumerate(annual_dates[1:]):
    date_0 = annual_dates[idx]
    nt_0 = net_profit.loc[date_0]
    nt_1 = net_profit.loc[date]
    data = (nt_1 - nt_0) / (np.abs(nt_0) + np.abs(nt_1))
    CHIN.loc[date] = data

O_score = pd.DataFrame(index=years, columns=logTA.columns)
for idx, date in enumerate(annual_dates):
    year = datetime.strptime(date, '%Y-%m-%d').year
    O_score.loc[str(year)] = -1.32 - 0.407 * logTA.loc[date] + 6.03 * TLTA.loc[date] - 1.43 * WCTA.loc[date] + \
                         0.076 * CLCA.loc[date] - 1.72 * OENEG.loc[date] - 2.37 * NITA.loc[date] - \
                         1.83 * FUTL.loc[date] + 0.285 * INTWO.loc[date] - 0.521 * CHIN.loc[date]
O_score = O_score
O_score.index.name = 'Date'
O_score_path = os.path.join(ARR_DATA, 'Ind', 'Annual', 'O_score.csv')

O_score.to_csv(O_score_path)
