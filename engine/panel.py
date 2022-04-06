import pandas as pd

from engine.basic import select_portfolio
from utils.date import *


def period_panel(portfolios, ret, mkt_val):
    """
    calculate the panel given stocks, period, and weighting methods
    :param portfolios: list of [period, stock_ids] pair
    :param ret: return
    :param mkt_val: Market value
    :return: time series of the weighted average return
    """
    panel = {}
    for name, p in portfolios.items():
        cur_data = pd.Series()
        for period, StkIds in p:
            cur_data = cur_data.append(weighted_return(ret, mkt_val, period, StkIds))
        panel[name] = cur_data

    return pd.DataFrame(panel)


def weighted_return(ret_val_all, mkt_val_all, period, stkIds):
    mkt_val = select_portfolio(mkt_val_all, period, stkIds)
    ret_val = select_portfolio(ret_val_all, period, stkIds)
    return (mkt_val * ret_val).sum(axis=1) / mkt_val.sum(axis=1)
    # return ret_val.mean(axis=1)


if __name__ == '__main__':
    # period_panel(
    #     {'S':
    #         [
    #             (['1999-01-01', '2000-01-01'], ['000001', '000002']),
    #             (['2000-01-01', '2001-01-01'], ['000002', '000005'])
    #         ]
    #     }
    # )
    pass