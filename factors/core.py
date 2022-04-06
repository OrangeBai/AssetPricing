from engine.IO import *
from functools import wraps


def annual_and_quarter_func(annual_or_quarter, pre, name, func, *args, **kwargs):
    """
    calculate the annual and quarterly factors according to func and *args, **kwargs
    :param annual_or_quarter: annual or quarterly
    :param pre: how many period before t_0 are required,
                    pre = 1 suggests that data of t_0 and t_1 are needed for calculation of factor
                    pre = 2 suggests that  data of t_0, t-1 and t-2 are needed for calculation of factor
    :param name: factor name
    :param func: function to computer the factor
    :param args: arguments passing to function
    :param kwargs: key words arguments passing to function
    :return:
    """
    if annual_or_quarter == 'A':
        statement_dates = statement_date_annual()
        keys = [datetime.strptime(date, '%Y-%m-%d').strftime('%Y') for date in statement_dates]
        factor_dict = dict.fromkeys(keys)
        output_path = os.path.join(ARR_DATA, 'Ind', 'Annual', name + '.csv')
    elif annual_or_quarter == 'Q':
        statement_dates = statement_date_quarter()
        keys = [datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m') for date in statement_dates]
        factor_dict = dict.fromkeys(keys)
        output_path = os.path.join(ARR_DATA, 'Ind', 'Quarterly', name + '.csv')
    elif annual_or_quarter == 'M':
        statement_dates = statement_date_monthly()
        keys = [datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m') for date in statement_dates]
        factor_dict = dict.fromkeys(keys)
        output_path = os.path.join(ARR_DATA, 'Ind', 'Monthly', name + '.csv')
    else:
        raise ValueError
    # first, set up the required dates in terms of [T0, T-1, T-2, ...,]
    # dates:    'yyyy-mm-dd'
    # date_ym:  'yyyy-mm'
    # date_y:   'yyyy'
    for idx, date in enumerate(statement_dates[pre:]):
        if pre != 0:
            dates = [statement_dates[i] for i in range(idx, idx + pre + 1)]
        else:
            dates = [statement_dates[idx]]
        dates.reverse()
        dates_dt = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        dates_ym = [date.strftime('%Y-%m') for date in dates_dt]
        dates_y = [date.strftime('%Y') for date in dates_dt]
        date_dict = {'dates': dates, 'dates_ym': dates_ym, 'dates_y': dates_y}

        if annual_or_quarter == 'A':
            factor_dict[dates_y[0]] = func(*args, **kwargs, **date_dict)
        else:
            factor_dict[dates_ym[0]] = func(*args, **kwargs, **date_dict)
    factor = pd.DataFrame(factor_dict).T
    factor.index.name = 'Date'
    factor.to_csv(output_path)
    return


def unpack_dates(**kwargs):
    kw_keys = kwargs.keys()
    assert 'dates' in kw_keys and 'dates_ym' in kwargs and 'dates_y' in kwargs
    return kwargs['dates'], kwargs['dates_ym'], kwargs['dates_y']

# This is a decorator version, but its too complex
# def annual_and_quarter_op(annual_or_quarter, pre, name):
#     def decorator(func):
#         @wraps(func)
#         def wrapped_func(*args, **kwargs):
#             if annual_or_quarter == 'A':
#                 statement_dates = statement_date_annual()
#                 output_path = os.path.join(ARR_DATA, 'Ind', 'Annual', name + '.csv')
#             else:
#                 statement_dates = statement_date_quarter()
#                 output_path = os.path.join(ARR_DATA, 'Ind', 'Quarterly', name + '.csv')
#
#             factor_dict = {}
#             for idx, date in enumerate(statement_dates[pre:]):
#                 if pre != 0:
#                     dates = statement_dates[idx - pre:idx]
#                 else:
#                     dates = [statement_dates[idx]]
#                 dates.reverse()
#                 dates_dt = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
#                 dates_ym = [date.strftime('%Y-%m') for date in dates_dt]
#                 dates_y = [date.strftime('%Y') for date in dates_dt]
#                 date_dict = {'dates': dates, 'dates_ym': dates_ym, 'dates_y': dates_y}
#                 if annual_or_quarter == 'A':
#                     factor_dict[dates_y[0]] = func(*args, **kwargs, **date_dict)
#                 else:
#                     factor_dict[dates_ym[0]] = func(*args, **kwargs, **date_dict)
#             factor = pd.DataFrame(factor_dict).T
#             factor.index.name = 'Date'
#             factor.to_csv(output_path)
#
#             return
#
#         return wrapped_func
#
#     return decorator
