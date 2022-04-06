from engine.IO import *

current_asset = get_statement_val('A001100000')
cash = get_statement_val('A001101000')
current_liability = get_statement_val('A002100000')

accrual = current_asset - cash - current_liability
total_asset = get_statement_val('A001000000')

stock_ids = intersection(total_asset.columns, total_asset.columns)
stock_ids.sort()
annual_statement_dates = list(total_asset.index)
years = get_year_tags()

total_accrual = pd.DataFrame(index=years, columns=stock_ids)
for idx, date in enumerate(annual_statement_dates[1:]):
    year = datetime.strptime(date, '%Y-%m-%d').year
    date_t_1 = annual_statement_dates[idx]

    asset_t = total_asset.loc[date]
    asset_t_1 = total_asset.loc[date_t_1]
    accrual_t = accrual.loc[date] * 2 / (asset_t_1 + asset_t)
    total_accrual.loc[str(year), :] = accrual_t[stock_ids]
    print(1)

total_accrual_path = os.path.join(ARR_DATA, 'Ind', 'Annual', 'total_accruals.csv')
total_accrual.to_csv(total_accrual_path)
print(1)
