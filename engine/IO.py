from utils.date import *

def get_statement_val(ID, consolidation='A', statement_time='year'):
    """
    get the data on balance sheet
    :param ID: Data ID: see BS_note
                    A001000000 [资产总计]           A002100000 [流动负债合计]
                    A002000000 [负债合计]           A001100000 [流动资产合计]
                    A001123000 [存货净额]           A001212000 [固定资产净额]
                    A001218000 [无形资产]
                    A001111000 [应收账款净额]
                    A001101000 [货币资金]
                    A002108000 [应付账款]
                    A001123000 [存货净额]
                Data ID: see IS_note
                    B001100000 [营业总收入]       B001101000 [营业收入]
                    B001200000 [营业总成本]       B001201000 [营业成本]
                    B002000000 [净利润]
    :param consolidation: consolidation or not: A＝合并报表、B＝母公司报表
    :param statement_time: year or quarter
    :return:
    """
    if ID[0] == 'A':
        path = os.path.join(RAW_DATA, 'Balance', 'BS.csv')
    else:
        path = os.path.join(RAW_DATA, 'Balance', 'IS.csv')
    statement = pd.read_csv(path, converters={'Stkcd': str})
    statement = statement[statement['Typrep'] == consolidation]

    data = statement.set_index(['Accper', 'Stkcd'])[ID].unstack()
    # if statement_time == 'year':
    #     valid_dates = intersection(statement_date_annual(), data.index)
    # else:
    #     valid_dates = intersection(statement_date_quarter(), data.index)
    # valid_dates.sort()
    # return data.loc[valid_dates]
    return data


def get_mkt_val(period, MktWgt_Id):
    """
    :param period: 'D' for daily, 'M' for monthly
    :param MktWgt_Id: Market value weighting method,
                        0: none,    1:circulation,    2: total
    :return:
    """
    if period == 'D':
        if MktWgt_Id == 1:
            mkt_wgt = 'Dsmvosd'
        else:
            mkt_wgt = 'Dsmvtll'

        mkt_path = os.path.join(ARR_DATA, 'Ret', 'Daily', mkt_wgt + '.csv')
        mkt_val_all = pd.read_csv(mkt_path, index_col='Trddt')

    else:
        Circulated_Id = 'Msmvosd' if MktWgt_Id == 1 else 'Msmvttl'
        ret_path = os.path.join(RAW_DATA, 'Ret', 'Monthly', 'TRD_Mnth.csv')
        data = pd.read_csv(ret_path, converters={'Stkcd': str})
        mkt_val_all = data.set_index(['Trdmnt', 'Stkcd'])[Circulated_Id].unstack()

    if not MktWgt_Id:
        mkt_val_all[pd.notna(mkt_val_all)] = 1
    return mkt_val_all


def get_ret(period, DivRe_Id=1):
    """
    :param period: 'M' for monthly, 'D' for daily
    :param DivRe_Id: Dividend reinvestment
                        0: no,      1: yes
    :return:
    """
    if period == 'D':
        div_re = 'Dretwd' if DivRe_Id else 'Dretnd'
        ret_path = os.path.join(ARR_DATA, 'Ret', 'Daily', div_re + '.csv')
        ret = pd.read_csv(ret_path, index_col='Trddt')
    else:
        div_re = 'Mretwd' if DivRe_Id else 'Mretnd'
        ret_path = os.path.join(RAW_DATA, 'Ret', 'Monthly', 'TRD_Mnth.csv')
        file = pd.read_csv(ret_path, converters={'Stkcd': str})
        ret = file.set_index(['Trdmnt', 'Stkcd'])[div_re].unstack()
    return ret


def get_turnover_file():
    """
    :return:
    """
    TO_path = os.path.join(ARR_DATA, 'Ind', 'Daily', 'Turnover.csv')
    TO = pd.read_csv(TO_path, index_col='TradingDate')
    return TO


def risk_free(RfType):
    data = pd.read_csv(os.path.join(ARR_DATA, 'Basic', 'TRD_Nrrate.csv'), index_col='Clsdt')
    if RfType == 'Daily':
        return data[data['Nrr1'] == 'NRI01']['Nrrdaydt']
    elif RfType == 'Weekly':
        return data[data['Nrr1'] == 'NRI01']['Nrrwkdt']
    elif RfType == 'Monthly':
        tags = get_month_tags()
        month_daily = data[data['Nrr1'] == 'NRI01']['Nrrmtdt']
        data = {}
        for tag in tags:
            try:
                data[tag] = month_daily[tag + '-01']
            except KeyError:
                pass
        return pd.Series(data)
    else:
        raise NameError('No risk free type named {0}'.format(RfType))


def market_return_daily(MktType, MktWgt_Id, DivRe_Id):
    """
    :param MktType:
                     1=上海A (不包含科创板），2=上海B，4=深圳A（不包含创业板），8=深圳B,  16=创业板， 32=科创板。
                     5=综合A股市场（不包含科创板、创业板）， 10=综合B股市场， 15=综合AB股市场， 21=综合A股和创业板； 31=综合AB股和创业；
                     37=综合A股和科创板； 47=综合AB股和科创板； 53=综合A股和创业板和科创板； 63=综合AB股和创业板和科创板。
    :param MktWgt_Id: Market value weighting method,
                        0: None,    1:total,    2: circulation
    :param DivRe_Id: Dividend reinvestment
                        0: no,      1: yes
    :return:
    """
    if MktType in [5, 10, 15, 21, 31]:
        data_path = os.path.join(ARR_DATA, 'Basic', 'TRD_Cndalym.csv')
        if MktWgt_Id == 0 and DivRe_Id == 1:
            field = 'Cdretwdeq'
        elif MktWgt_Id == 0 and DivRe_Id == 0:
            field = 'Cdretmdeq'
        elif MktWgt_Id == 1 and DivRe_Id == 1:
            field = 'Cdretwdos'
        elif MktWgt_Id == 1 and DivRe_Id == 0:
            field = 'Cdretmdos'
        elif MktWgt_Id == 2 and DivRe_Id == 1:
            field = 'Cmretwdos'
        elif MktWgt_Id == 2 and DivRe_Id == 0:
            field = 'Cdretmdtl'
        else:
            raise NameError('Field Not Found')
    elif MktType in [1, 2, 4, 8, 16, 32]:
        data_path = os.path.join(ARR_DATA, 'Basic', 'TRD_Dalym.csv')
        if MktWgt_Id == 0 and DivRe_Id == 1:
            field = 'Dretwdeq'
        elif MktWgt_Id == 0 and DivRe_Id == 0:
            field = 'Dretmdeq'
        elif MktWgt_Id == 1 and DivRe_Id == 1:
            field = 'Dretwdos'
        elif MktWgt_Id == 1 and DivRe_Id == 0:
            field = 'Dretmdos'
        elif MktWgt_Id == 2 and DivRe_Id == 1:
            field = 'Dretwdtl'
        elif MktWgt_Id == 2 and DivRe_Id == 0:
            field = 'Dretmdtl'
        else:
            raise NameError('Field Not Found')
    else:
        raise NameError('MktType Not Found')
    panel = pd.read_csv(data_path, index_col='Trddt')
    panel = panel[panel['Markettype'] == MktType][field]
    return panel


def market_return_monthly(MktType, MktWgt_Id, DivRe_Id):
    # TODO fix it
    """
    :param MktType:
                     1=上海A (不包含科创板），2=上海B，4=深圳A（不包含创业板），8=深圳B,  16=创业板， 32=科创板。
                     5=综合A股市场（不包含科创板、创业板）， 10=综合B股市场， 15=综合AB股市场， 21=综合A股和创业板； 31=综合AB股和创业；
                     37=综合A股和科创板； 47=综合AB股和科创板； 53=综合A股和创业板和科创板； 63=综合AB股和创业板和科创板。
    :param MktWgt_Id: Market value weighting method,
                        0: None,    1:total,    2: circulation
    :param DivRe_Id: Dividend reinvestment
                        0: no,      1: yes
    :return:
    """
    if MktType in [5, 10, 15, 21, 31]:
        data_path = os.path.join(ARR_DATA, 'Basic', 'TRD_Cnmont.csv')
        if MktWgt_Id == 0 and DivRe_Id == 1:
            field = 'Cdretwdeq'
        elif MktWgt_Id == 0 and DivRe_Id == 0:
            field = 'Cdretmdeq'
        elif MktWgt_Id == 1 and DivRe_Id == 1:
            field = 'Cdretwdos'
        elif MktWgt_Id == 1 and DivRe_Id == 0:
            field = 'Cdretmdos'
        elif MktWgt_Id == 2 and DivRe_Id == 1:
            field = 'Cmretwdos'
        elif MktWgt_Id == 2 and DivRe_Id == 0:
            field = 'Cmretmdos'
        else:
            raise NameError('Field Not Found')
    elif MktType in [1, 2, 4, 8, 16, 32]:
        data_path = os.path.join(ARR_DATA, 'Basic', 'TRD_Dalym.csv')
        if MktWgt_Id == 0 and DivRe_Id == 1:
            field = 'Dretwdeq'
        elif MktWgt_Id == 0 and DivRe_Id == 0:
            field = 'Dretmdeq'
        elif MktWgt_Id == 1 and DivRe_Id == 1:
            field = 'Dretwdos'
        elif MktWgt_Id == 1 and DivRe_Id == 0:
            field = 'Dretmdos'
        elif MktWgt_Id == 2 and DivRe_Id == 1:
            field = 'Dretwdtl'
        elif MktWgt_Id == 2 and DivRe_Id == 0:
            field = 'Dretmdtl'
        else:
            raise NameError('Field Not Found')
    else:
        raise NameError('MktType Not Found')
    panel = pd.read_csv(data_path, index_col='Trdmnt')
    panel = panel[panel['Markettype'] == MktType][field]
    return panel


def load_ind_annual(file, period, index_column='date'):
    file_path = os.path.join(ARR_DATA, 'Ind', period, file + '.csv')
    return pd.read_csv(file_path, index_col=index_column)

if __name__ == '__main__':
    get_statement_val('B002000000')
