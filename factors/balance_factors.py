from factors.core import *
from functools import reduce
from engine.basic import select_portfolio


# @annual_and_quarter_op('Q', 0, 'BM')
def get_BM(book, mv, **kwargs):
    dates, dates_ym, dates_y = unpack_dates(**kwargs)
    BM = book.loc[dates[0]] / (1000 * mv.loc[dates_ym[0]])
    return BM


def get_inv_to_asset(PPE, inventory, book_val, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)
    # change of PPE and inventory from T-1 to T-0
    change_of_PPE = PPE.loc[dates[0]] - PPE.loc[dates[1]]
    change_of_inv = inventory.loc[dates[0]] - inventory.loc[dates[1]]
    BV_lagged = book_val.loc[dates[1]]  # book value of year t-1
    return (change_of_PPE + change_of_inv.fillna(0)) / BV_lagged


def get_asset_growth(total_asset, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)
    ast0 = total_asset.loc[dates[0]]  # asset of year t
    ast_1 = total_asset.loc[dates[1]]  # asset of year t-1
    return (ast0 - ast_1) / ast_1


def get_net_issue(shares, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)
    return (shares.loc[dates_ym[0]] - shares.loc[dates_ym[1]]) / shares.loc[dates_ym[1]]


def get_op_asset(total_asset, fin_ast, op_debt, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)

    return (total_asset.loc[dates[0]] - fin_ast.loc[dates[0]] - op_debt.loc[dates[0]]) / total_asset.loc[dates[1]]


def get_RoA(total_ast, net_income, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)

    if dates[0] != dates[1]:
        # if not in same year, net income is not cumulated
        earning = net_income.loc[dates[0]]
    else:
        # else, subtract last quarter
        earning = net_income.loc[dates[0]] - net_income.loc[dates[-1]]
    return 2 * earning / (total_ast.loc[dates[-1]] + total_ast.loc[dates[-1]])


def get_RoE(equity, net_income, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)

    if dates[0] != dates[1]:
        # if not in same year, net income is not cumulated
        earning = net_income.loc[dates[0]]
    else:
        # else, subtract last quarter
        earning = net_income.loc[dates[0]] - net_income.loc[dates[-1]]
    return 2 * earning / (equity.loc[dates[-1]] + equity.loc[dates[-1]])


def get_Momentum(Ret, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)
    past_ret = Ret.loc[dates_ym[1:]]

    return past_ret.mean()


def get_turnover(turnover, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)
    past_ret = select_portfolio(turnover, [dates_ym[-1], dates_ym[0]])

    return past_ret.mean()


def get_tvol(ret, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)
    past_ret = select_portfolio(ret, [dates_ym[-1], dates_ym[0]])

    return past_ret.var()




def get_gross_profit(total_ast, gross_profit, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)

    if dates[0] != dates[1]:
        # if not in same year, net income is not cumulated
        earning = gross_profit.loc[dates[0]]
    else:
        # else, subtract last quarter
        earning = gross_profit.loc[dates[0]] - gross_profit.loc[dates[-1]]
    return earning / (total_ast.loc[dates[-1]] + total_ast.loc[dates[-1]])


def get_MV(MV, **kwargs):
    # unpack dates, note that dates[0] is current year, dates[i] is T-i
    dates, dates_ym, dates_y = unpack_dates(**kwargs)
    return MV.loc[dates_ym[0]]


# @annual_and_quarter_op('Q', 0, 'BM')
def get_BM_quarter(equity=None, mv=None, dates=None, dates_ym=None, dates_y=None):
    return equity.loc[dates[0]] / (1000 * mv.loc[dates_ym[0]])

# total_asset = get_statement_val('A001000000')
# total_liability = get_statement_val('A002000000')
#
#
# annual_and_quarter_func('A', 0, 'BM', get_BM, )
#
# if __name__ == '__main__':
#     total_asset = get_statement_val('A001000000')
#     total_liability = get_statement_val('A002000000')
#
#     equity_file = total_asset - total_liability
#     mv_file = get_monthly_mv(0)
#
#     get_BM_annual(equity_file, mv_file)
#     get_BM_quarter(equity_file, mv_file)
