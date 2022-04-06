from config import *
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta


# TODO:
#       refactor date module and IO module


def get_trade_dates(start, end):
    """
    get all trade dates from start date to end date
    :param start: start date
    :param end: end date
    :return: a list of trading dates ['yyyy-mm-dd', 'yyyy-mm-dd', ..., 'yyyy-mm-dd']
    """
    date_file = os.path.join(ARR_DATA, 'Basic', 'TRD_Cale.csv')
    dates = pd.read_csv(date_file)
    open_dates = dates[dates['State'] == 'O']
    open_dates = open_dates['Clddt'].unique().tolist()
    for date in open_dates:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except Exception as e:
            print(e)
            open_dates.rempve(date)
    required_trade_dates = [date for date in open_dates if start <= date < end]
    return required_trade_dates


def statement_date_annual():
    return [str(i) + '-12-31' for i in range(1990, 2022)]


def statement_date_quarter():
    period_1 = [str(y) + m for y in range(1990, 1994) for m in ['-12-31']]
    period_2 = [str(y) + m for y in range(1994, 2002) for m in ['-06-30', '-12-31']]
    period_3 = [str(y) + m for y in range(2002, 2022) for m in ['-03-31', '-06-30', '-09-30', '-12-31']]
    return period_1 + period_2 + period_3


def statement_date_monthly():
    year_tag = [str(i) for i in range(1991, 2023)]
    months = list(range(1, 13))
    all_tags = [y + '-' + str(m).zfill(2) + '-01' for y in year_tag for m in months]
    return ['1990-12-01'] + all_tags


def get_year_tags(st=1990, ed=2022):
    return [str(i) for i in range(st, ed)]


def get_month_tags(st='1990-01', ed='2022-01'):
    year_tag = [str(i) for i in range(1990, 2023)]
    months = list(range(1, 13))
    all_tags = [y + '-' + str(m).zfill(2) for y in year_tag for m in months]
    return all_tags


def get_quarter_tags(st=1990, ed=2022):
    year_tag = [str(i) for i in range(1990, 2023)]
    quarters = ['03', '06', '09', '12']
    quarters = [y + '-' + q for y in year_tag for q in quarters]
    return quarters


def get_year_splits(st=1990, ed=2022):
    year_tags = [str(i) for i in range(st, ed)]
    return get_splits([tag for tag in year_tags if str(st) <= tag <= str(ed)])


def get_month_splits(st='1990-01', ed='2022-01'):
    year_tag = [str(i) for i in range(1990, 2023)]
    months = list(range(1, 13))
    all_tags = [y + '-' + str(m).zfill(2) for y in year_tag for m in months]
    return get_splits([tag for tag in all_tags if str(st) <= tag <= str(ed)])


def get_splits(tags):
    """
    get the first trading dates for each year
    :return: ['1990', '1991', '1992', ... , '2021']
    """
    dates = get_trade_dates(tags[0], tags[-1])
    trading_dates = [get_nearest_date(dates, tags[idx], tags[idx + 1]) for idx in range(len(tags) - 1)]
    return [date for date in trading_dates if date is not None]


def tags_to_periods(tags):
    """
    Convert a list of dates to a list of periods with format: (start, end)
    :param tags: [date_1, date_2, ..., date_n]
    :return: [(date_1, date_2), (date_2, date_3), ..., (date_n-1, date_n)]
    """
    return [(tags[idx], tags[idx + 1]) for idx in range(len(tags) - 1)]


def get_nearest_date(dates, start_time, end_time):
    """
    for a list of dates, find the nearest date
    :param dates: a list of dates
    :param start_time: start date of the period
    :param end_time: end date of the period
    :return:
    """
    dates.sort()
    for date in dates:
        if start_time <= date < end_time:
            return date


def month_to_date(tags):
    """
    convert month-year format to yyyy-mm
    :param tags: month-year format: 'Jun-1999'
    :return: yyyy-mm format: 1999-06
    """
    pattern = re.compile(r'([a-zA-Z]*)-([0-9]*)')
    m = re.search(pattern, tags)
    try:
        date = year_dict(m.group(2)) + '-' + month_dict(m.group(1))
        return date
    except TypeError or KeyError as e:
        print('Something wrong:{0}'.format(e))


def year_dict(year):
    """
    for month_to_date, convert yy to yyyy
    :param year: 99 -> 1999, 10 -> 2010
    :return:
    """
    if int(year) > 80:
        return '19' + str(year)
    else:
        return '20' + str(year)


def month_dict(month):
    """
    for month_to_date, convert month to Arabic numerals
    :param month: 'Jan' -> '01', 'Feb' -> '02'
    :return:
    """
    return {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }[month]


def get_nearest_feature(dataframe, start_time, end_time=None):
    try:
        if end_time:
            valid = np.logical_and(dataframe.index >= start_time, dataframe.index < end_time)
            index = dataframe[valid].index.sort_values()[0]
        else:
            index = dataframe[dataframe.index >= start_time].index.sort_values()[0]
        return dataframe.loc[index]
    except IndexError as e:
        print(e)


def intersection(*args):
    """
    Calculate the intersection of a set of stock ids
    :param args: [stock_ids_1], [stock_ids_2], ....
    :return:
    """
    return list(set.intersection(*[set(arg) for arg in args]))


def str_date_to_list(date):
    """
    convert str time to a list
    :param date: 'yyyy-mm-dd'
    :return: [yyyy, mm, dd]
    """
    return [int(date) for date in date.split('-')]


def cal_feature(dataframe, long, short):
    return (dataframe[long].sum(axis=1) - dataframe[short].sum(axis=1)) / len(long)


def annual_statement_mapping():
    """
    Deadline of financial statement is 4.30.
    For factor calculated from statements of year T, the valid period is from year T+1 May to T+2 April
    :return: {
                year_1[yyyy]: (start_1[yyyy-mm], end_1[yyyy-mm], ...
                year_n[yyyy]: (start_n[yyyy-mm], end_n[yyyy-mm]
            }
    """
    year_tags = get_year_tags()
    mapping = {}
    for date in year_tags:
        date_dt = datetime.strptime(date, '%Y')
        start_dt = datetime(year=date_dt.year + 1, month=6, day=1)
        end_dt = datetime(year=date_dt.year + 2, month=6, day=1)

        start = datetime.strftime(start_dt, '%Y-%m')
        end = datetime.strftime(end_dt, '%Y-%m')
        mapping[date] = (start, end)
    return mapping


if __name__ == '__main__':
    a = get_year_splits()
    b = get_month_splits()
    c = get_splits(a)
    d = get_splits(b)
    print(1)
