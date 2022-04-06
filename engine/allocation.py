import numpy as np
from engine.panel import *
from engine.basic import *
import time
import itertools as it


def allocate_stocks_(StkIds, feature, partition):
    # TODO:
    #       refactor
    stk_ids = intersection(feature.index, StkIds)

    sorted_features = feature.loc[stk_ids].sort_values()
    stock_idx = [int(par * len(sorted_features)) for par in partition]
    allocation = []
    for idx, _ in enumerate(stock_idx[:-1]):
        allocation += [list(sorted_features[stock_idx[idx]: stock_idx[idx + 1]].index)]

    return allocation


def allocate_single_period_mixed(StkIds, features, partitions, names):
    """
    Allocate StkIds according to features and partition
    :param StkIds:
    :param period:
    :param features:
    :param partition:
    :param names:
    :return:
    """
    allocation = {}
    groups = []
    for f, par in zip(features, partitions):
        groups.append(allocate_stocks_(StkIds, f, par))
    groups_names = [len(par) - 1 for par in partitions]
    for idxes in it.product(*[list(range(g)) for g in groups_names]):
        cur_name = ''.join([name + str(idx) for name, idx in zip(names, idxes)])
        p = intersection(*[groups[i][idx] for i, idx in enumerate(idxes)])
        allocation[cur_name] = p
    return allocation


def allocate_all(zipped_data, partitions, names):
    allocation = {}
    for period, StkIds, features in zipped_data:
        cur_allocation = allocate_single_period_mixed(StkIds, features, partitions, names)
        for name, Stk in cur_allocation.items():
            if name not in allocation.keys():
                allocation[name] = [(period, Stk)]
            else:
                allocation[name].append((period, Stk))
    return allocation


#
# def allocate_mixed(StkIds, periods, features, partition, names):
#     # TODO:
#     #       refactor
#     allocation = {}
#     mkt_val_all = get_mkt_val(0)
#     ret_val_all = get_daily_ret_val(1)
#     for (start, end), feature in zip(periods, features):
#         t = time.time()
#         available = ret_val_all[np.logical_and(ret_val_all.index >= start, ret_val_all.index < end)]
#         data_available = available.columns[((available.isna().sum()) <= 5)].to_list()
#         companies = retrieve_company(start)
#         companies = intersection(companies, data_available)
#         temp_allocation = []
#         for f, par in zip(feature, partition):
#             temp_allocation += [(allocate_stocks_(companies, f, par))]
#         groups = [len(par) - 1 for par in partition]
#         for idxes in it.product(*[list(range(g)) for g in groups]):
#             n = ''.join([name + str(idx) for name, idx in zip(names, idxes)])
#             p = intersection(*[temp_allocation[i][idx] for i, idx in enumerate(idxes)])
#             if n not in allocation.keys():
#                 allocation[n] = []
#             allocation[n].append([(start, end), p])
#     return allocation

def allocate_multiple(StkIds, features, partitions, name, prefix=''):
    """
    Allocate stocks for a given period, and a set of features and partition ratios
    :param StkIds: Stock Ids
    :param features: the feature according to which the allocation is performed
    :param partitions: ratio of different stocks
    :param name: Name of the feature
    :param prefix: parent set the portfolios belong to
    :return: a dictionary:
                {
                    name_1: [stock_1, stock_2,..., stock_n],
                    name_2: [stock_1, stock_2,..., stock_n],
                                        ...
                    name_n: [stock_1, stock_2,..., stock_n],
                }
    """
    all_portfolios = {}
    for idx, (name, feature, partitions) in enumerate(zip(name, features, partitions)):
        if idx == 0:
            all_portfolios.update(allocate_stocks(StkIds, feature, partitions, name, prefix))
        else:
            layer_portfolios = {}
            for key, val in all_portfolios.items():
                layer_portfolios.update(allocate_stocks(val, feature, partitions, name, key))
            all_portfolios = layer_portfolios
    return all_portfolios


def allocate_stocks(StkIds, feature, partition, name, prefix=''):
    """
    Allocate stocks for a given period, feature and partition ratio
    :param StkIds: Stock Ids
    :param feature: the feature according to which the allocation is performed
    :param partition: ratio of different stocks
    :param name: Name of the feature
    :param prefix: parent set the portfolios belong to
    :return: a dictionary:
                {
                    name_1: [stock_1, stock_2,..., stock_n],
                    name_2: [stock_1, stock_2,..., stock_n],
                                        ...
                    name_n: [stock_1, stock_2,..., stock_n],
                }
    """
    stk_ids = intersection(feature.index, StkIds)

    sorted_features = feature.loc[stk_ids].sort_values()
    stock_idx = [int(par * len(sorted_features)) for par in partition]

    allocation = {}
    for idx, _ in enumerate(stock_idx[:-1]):
        allocation[prefix + name + str(idx)] = list(sorted_features[stock_idx[idx]: stock_idx[idx + 1]].index)

    return allocation


if __name__ == '__main__':
    turnover = pd.read_csv(r'E:\Dataset\CSMAR\Arranged\Ind\Daily\Turnover.csv', index_col='TradingDate')
    PB = pd.read_csv(r'E:\Dataset\CSMAR\Arranged\Ind\Daily\PB.csv', index_col='TradingDate')

    get_nearest_feature(PB, '2000-01-01', '2001-01-01')
    # portfolios = allocate_single_period(PB.columns, period=['2000-01-01', '2001-01-01'], features=[turnover, PB],
    #                                     partitions=[[0, 0.3, 0.7, 1], [0, 0.3, 0.7, 1]], name=['turnover', 'PB'])
    #
    # for key, val in portfolios.items():
    #     portfolios[key] = [(['2000-01-01', '2001-01-01'], val)]
    #
    # bb = period_panel(portfolios)
    print(1)
