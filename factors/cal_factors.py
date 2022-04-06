from factors.core import *
from factors.balance_factors import *

total_asset = get_statement_val('A001000000')
total_debt = get_statement_val('A002000000')
book_value = total_asset - total_debt
mv = get_mkt_val('M', 1)

# annual_and_quarter_func('A', 0, 'BM', get_BM, book_value, mv)
# annual_and_quarter_func('Q', 0, 'BM', get_BM, book_value, mv)
# PPE = get_statement_val('A001212000')
# Inventory = get_statement_val('A001123000')
#
# annual_and_quarter_func('A', 1, 'InvToAst', get_inv_to_asset, PPE, Inventory, book_value)
# annual_and_quarter_func('Q', 1, 'InvToAst', get_inv_to_asset, PPE, Inventory, book_value)
#
# annual_and_quarter_func('A', 1, 'AstGrowth', get_asset_growth, total_asset)
# annual_and_quarter_func('Q', 1, 'AstGrowth', get_asset_growth, total_asset)

# # ret ret monthly
# ret_path = os.path.join(RAW_DATA, 'Ret', 'Monthly', 'TRD_Mnth.csv')
# data = pd.read_csv(ret_path, converters={'Stkcd': str})
# Cls_prc = data.set_index(['Trdmnt', 'Stkcd'])['Mclsprc'].unstack()
#
# shares = mv / Cls_prc
#
# annual_and_quarter_func('A', 1, 'NetIssue', get_net_issue, shares)
# annual_and_quarter_func('Q', 1, 'NetIssue', get_net_issue, shares)

# # %%%%%%%%%%%%%%%%%%%%%%  Return Over Asset %%%%%%%%%%%%%%%%%%%%%%%%
# net_income = get_statement_val(ID='B002000000')
#
# annual_and_quarter_func('A', 1, 'RoA', get_RoA, total_asset, net_income)
# annual_and_quarter_func('Q', 1, 'RoA', get_RoA, total_asset, net_income)
# print(1)
#
# # %%%%%%%%%%%%%%%%%%%%%%  Return Over Equity %%%%%%%%%%%%%%%%%%%%%%%%
net_income = get_statement_val(ID='B002000000')

annual_and_quarter_func('A', 1, 'RoE', get_RoE, book_value, net_income)
annual_and_quarter_func('Q', 1, 'RoE', get_RoE, book_value, net_income)

# # %%%%%%%%%%%%%%%%%%%%%%  Momentum %%%%%%%%%%%%%%%%%%%%%%%%
net_income = get_statement_val(ID='B002000000')

ret_Monthly = get_ret('M')
annual_and_quarter_func('M', 11, 'Momentum_11', get_Momentum, ret_Monthly)
annual_and_quarter_func('M', 5, 'Momentum_6', get_Momentum, ret_Monthly)
#
# # %%%%%%%%%%%%%%%%%%%%%%  Turnover %%%%%%%%%%%%%%%%%%%%%%%%
turnover = get_turnover_file()

annual_and_quarter_func('M', 1, 'turnover_1', get_turnover, turnover)
annual_and_quarter_func('M', 2, 'turnover_2', get_turnover, turnover)
annual_and_quarter_func('M', 3, 'turnover_3', get_turnover, turnover)


# %%%%%%%%%%%%%%%%%%%%%%  Tvol %%%%%%%%%%%%%%%%%%%%%%%%
ret_Daily = get_ret('D')

annual_and_quarter_func('M', 1, 'tvol_1', get_tvol, ret_Daily)
annual_and_quarter_func('M', 2, 'tvol_2', get_tvol, ret_Daily)
annual_and_quarter_func('M', 3, 'tvol_3', get_tvol, ret_Daily)

# ################## Net Operating Asset#############################
# fin_ast_ids = ['A001202000', 'A001203000', 'A001204000', 'A001205000', 'A001206000', 'A001211000']
# fin_ast_files = [get_statement_val(f).fillna(0) for f in fin_ast_ids]
# fin_ast = reduce(lambda x, y: x.add(y, fill_value=0), fin_ast_files)
#
# op_debt_ids = ['A002101000', 'A002107000', 'A002108000', 'A002109000', 'A002112000', 'A002201000', 'A002208000']
# op_debt = [get_statement_val(f).fillna(0) for f in op_debt_ids]
# op_debt = reduce(lambda x, y: x.add(y, fill_value=0), op_debt)
#
# annual_and_quarter_func('A', 1, 'NetOpAst', get_op_asset, total_asset, fin_ast, op_debt)
# annual_and_quarter_func('Q', 1, 'NetOpAst', get_op_asset, total_asset, fin_ast, op_debt)
#
# # %%%%%%%%%%%%%%%%%%%%%%  Gross Profit to Asset %%%%%%%%%%%%%%%%%%%%%%%%
# op_income = get_statement_val('B001101000')
# op_expense = get_statement_val('B001201000')
# gross_profit = op_income - op_expense
#
# annual_and_quarter_func('A', 1, 'GrossPro', get_gross_profit, total_asset, gross_profit)
# annual_and_quarter_func('Q', 1, 'GrossPro', get_gross_profit, total_asset, gross_profit)
#
# MV = get_mkt_val('M', 1)
# annual_and_quarter_func('A', 0, 'MV', get_MV, MV)
# annual_and_quarter_func('Q', 0, 'MV', get_MV, MV)
# print(1)
