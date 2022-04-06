from datetime import timedelta
from config import *

from utils.date import *


def retrieve_company(cur_date, interval=365, NotIndCd=None, MktType=None):
    """
    Select available stocks on current date
    :param interval:
    :param cur_date:
    :param NotIndCd: Industry code to exclude:
                        1: banking,             3: real estate
    :param MktType: stocks list on which board:
                        1: Shanghai A board,    2: Shanghai B board
                        4: Shenzhen A board,    8: Shenzhen B board
                        16:Growth Enterprise Board
                        32:Sci-Tech innovation board
    :return: Stock Ids
    """
    if MktType is None:
        MktType = [1, 4, 16]
    if NotIndCd is None:
        NotIndCd = [1, 3]
    file_path = os.path.join(RAW_DATA, 'Basic', 'TRD_Co.csv')
    data = pd.read_csv(file_path, converters={'Stkcd': str})

    td = timedelta(days=interval)
    list_before = (cur_date - td).strftime('%Y-%M-%d')
    data = data[data['Listdt'] < list_before]

    ind_cd_idx = np.all([data['Indcd'] != i for i in NotIndCd], axis=0)
    data = data[ind_cd_idx]

    mkt_type_idx = np.any([data['Markettype'] == i for i in MktType], axis=0)
    data = data[mkt_type_idx]
    return data['Stkcd']


def select_date(data_frame, date_name, period):
    """
    Select all entities that within the period
    :param data_frame: Input dataframe with a trading date columns
    :param date_name: Column name of the date data
    :param period: [start date(included), end_date(excluded)]
    :return: data
    """
    data = data_frame[np.logical_and(data_frame[date_name] >= period[0], data_frame[date_name] < period[1])]
    return data


def remove_na(period, ret, mkt, maximum_na=3):
    na_ret = select_portfolio(ret, period)
    ret_ids = na_ret.loc[:, na_ret.isna().sum() <= maximum_na].columns
    na_mkt = select_portfolio(mkt, period)
    mkt_ids = na_mkt.loc[:, na_mkt.isna().sum() <= maximum_na].columns
    return intersection(ret_ids, mkt_ids)


def remove_factor_na(date, factors):
    return intersection(*[factor.loc[:, ~factor.loc[date].isna()].columns for factor in factors])


def drop_shell_company(MV, date, available):
    available = MV.loc[date, available].dropna().sort_values().index
    available = available[-int(0.7 * len(available)):]
    return available


def zip_data(mapping, ret, mkt, MV, factors, remove_shell, na_num=3):
    """
    :param mapping:mapping is the date: (start, end) pair
    :param ret: ret and mkt are data for computing return
    :param mkt:
    :param MV: MV is for removing shell company
    :param factors: factors
    :param remove_shell: if 1 then remove small companies
    :param na_num: maximum tolerance of na values
    :return: per
    """
    zipped_data = []
    for date, period in mapping.items():
        StkIds = retrieve_company(datetime.strptime(period[0], '%Y-%m'))
        not_na = remove_na(period, ret, mkt, maximum_na=na_num)
        not_factor_na = remove_factor_na(date, factors)
        if remove_shell:
            not_small = drop_shell_company(MV, date, StkIds)
            StkIds = intersection(StkIds, not_na, not_factor_na, not_small)
        else:
            StkIds = intersection(StkIds, not_na, not_factor_na)
        features = [feature.loc[date] for feature in [MV] + factors]
        zipped_data.append([period, StkIds, features])
    return zipped_data


def select_portfolio(data_frame, period, StkIds=None):
    """
    Select a sub-dataframe according to period and stock ids
    :param data_frame:
                        index: trading date, columns: stock ids

    :param period: [start date(included), end_date(excluded)]
    :param StkIds: a list of stocks
    :return: dataframe
    """
    data = data_frame[np.logical_and(data_frame.index >= period[0], data_frame.index < period[1])]
    if StkIds is not None:
        stk_ids = intersection(StkIds, data.columns)
    else:
        stk_ids = data.columns
    return data.loc[:, stk_ids]


def select_entity(data_frame, index, StkIds, value_name):
    """
    Generate dataframe with index: trading date, columns: stock ids
    :param data_frame: input dataframe
    :param index: key name of the index
    :param StkIds: key name of the stock ids
    :param value_name: key name of the value
    :return:
    """
    data_frame = data_frame.set_index(index)[value_name].unstack()

    return data_frame.loc[:, StkIds]
