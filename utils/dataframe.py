def get_keys(data_field):
    if data_field == 'Ret':
        return 'Stkcd', 'Trddt'
    elif data_field == 'Ind':
        return 'Symbol', 'TradingDate'
    else:
        raise NameError()
