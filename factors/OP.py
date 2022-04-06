from engine.IO import *
from utils.date import *

total_asset = get_statement_val(ID='A001000000', statement_time='year')
net_income = get_statement_val(ID='B002000000', statement_time='year')

stock_ids = intersection(total_asset.columns, net_income.columns)
stock_ids.sort()
annual_statement_dates = list(total_asset.index)
years = get_year_tags()

OP = pd.DataFrame(index=years, columns=stock_ids)
for idx, date in enumerate(annual_statement_dates):
    year = datetime.strptime(date, '%Y-%m-%d').year
    net_income_t = net_income.loc[date]
    asset_t = total_asset.loc[date]
    inv_t = net_income_t / asset_t
    OP.loc[str(year), :] = inv_t[stock_ids]
    print(1)
OP.index.name = 'Date'
OP_path = os.path.join(ARR_DATA, 'Ind', 'Annual', 'Operating_Profit.csv')
OP.to_csv(OP_path)
