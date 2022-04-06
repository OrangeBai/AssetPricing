import os.path
import shutil

import pandas as pd

from engine.IO import *
from engine.allocation import *
from engine.basic import *
from engine.regression import *
import argparse
from utils.regression import *


def annual_reg(args):
    mapping = annual_statement_mapping()

    ret = get_ret('M', 1)
    mkt = get_mkt_val('M', 1).shift(1)

    rf = risk_free('Monthly')
    rm = market_return_monthly(5, 2, 1)

    MV_path = os.path.join(ARR_DATA, 'Ind', 'Annual', 'MV.csv')
    MV = pd.read_csv(MV_path, converters={'Date': str}).set_index('Date')

    factors = get_3factor_annual(remove_shell=1)
    anomaly = get_panel([args.anomaly], args.anomaly_groups, remove_shell=1)

    if args.anomaly_groups[0] == 1:
        anomaly.to_csv(os.path.join(RES_DIR, 'des', '10', args.anomaly + '.csv'))
    elif args.anomaly_groups[0] == 2 and args.anomaly_groups[1] == 10:
        anomaly.to_csv(os.path.join(RES_DIR, 'des', '20', args.anomaly + '.csv'))

    cur_fac = factors.loc[args.st: args.ed]
    res = {}
    for name, p in anomaly.iteritems():
        y = (p - rf / 100).loc[args.st: args.ed]
        res[name] = regression(y, cur_fac)

    param, t, p, r, r_adj = {}, {}, {}, {}, {}
    for key, val in res.items():
        param[key] = val.params
        t[key] = val.tvalues
        p[key] = val.pvalues
        r[key] = val.rsquared
        r_adj[key] = val.rsquared_adj
    if args.anomaly_groups[1] == 5:
        res_dir = os.path.join(RES_DIR, '5', args.anomaly)
    else:
        res_dir = os.path.join(RES_DIR, '10', args.anomaly)
    if os.path.exists(res_dir):
        shutil.rmtree(res_dir)
    os.makedirs(res_dir)
    pd.DataFrame(param).to_csv(os.path.join(res_dir,  'param.csv'))
    pd.DataFrame(t).to_csv(os.path.join(res_dir, 't.csv'))
    pd.DataFrame(p).to_csv(os.path.join(res_dir,  'p.csv'))
    # pd.DataFrame(r).to_latex(os.path.join(res_dir,  'r.tex'))
    # pd.DataFrame(r_adj).to_latex(os.path.join(res_dir, 'r_adj.tex'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--anomaly', type=str, default='O_score')
    parser.add_argument('--anomaly_groups', type=int, nargs='*', default=[5, 5])
    parser.add_argument('--st', type=str, default='1997-01')
    parser.add_argument('--ed', type=str, default='2021-11')
    for name in ['AstGrowth', 'BM', 'GrossPro', 'InvToAst', 'NetIssue', 'NetOpAst', 'O_score', 'RoA']:
        annual_reg(parser.parse_args(['--anomaly', name]))

    print(1)
