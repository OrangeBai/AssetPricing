import numpy as np
from config import *
import pandas as pd
from engine.IO import *
from engine.basic import *
from engine.allocation import *


def get_partition(factor_groups):
    partition = []
    for num in factor_groups:
        if num == 1:
            partition.append([0, 1])
        elif num == 2:
            partition.append([0, 0.5, 1])
        elif num == 3:
            partition.append([0, 0.3, 0.7, 1])
        elif num == 5:
            partition.append(list(np.arange(0, 1.2, 0.2)))
        elif num == 10:
            partition.append(list(np.arange(0, 1.1, 0.1)))
        else:
            raise NameError
    return partition


def load_factors(factor_names):
    factors = []
    for factor in factor_names:
        # get features
        BM_path = os.path.join(ARR_DATA, 'Ind', 'Annual', factor + '.csv')
        factors.append(pd.read_csv(BM_path, converters={'Date': str}).set_index('Date'))
    return factors


def get_3factor_annual(remove_shell=0):
    rf = risk_free('Monthly')
    rm = market_return_monthly(5, 2, 1)
    factor_panel = get_panel(['BM'], [2, 3], remove_shell=0)

    HML = cal_feature(factor_panel, ['MV0BM2', 'MV1BM2'], ['MV0BM0', 'MV1BM0'])
    SMB = cal_feature(factor_panel, ['MV0BM1', 'MV0BM1', 'MV0BM2'], ['MV1BM1', 'MV1BM1', 'MV1BM2'])
    factors = pd.DataFrame(data={'MKT': rm - rf / 100, 'HML': HML, 'SMB': SMB})
    return factors


def get_panel(names, groups, weight_id=1, remove_shell=0):
    assert len(names) + 1 == len(groups)

    MV_path = os.path.join(ARR_DATA, 'Ind', 'Annual', 'MV.csv')
    MV = pd.read_csv(MV_path, converters={'Date': str}).set_index('Date')

    mapping = annual_statement_mapping()
    ret = get_ret('M', 1)
    mkt = get_mkt_val('M', weight_id).shift(1)

    factor = load_factors(names)
    anomaly_par = get_partition(groups)

    zipped_ano = zip_data(mapping, ret, mkt, MV, factor, remove_shell=remove_shell, na_num=1)
    anomaly_allocation = allocate_all(zipped_ano, anomaly_par, ['MV'] + names)
    anomaly_panel = period_panel(anomaly_allocation, ret, mkt)
    return anomaly_panel
