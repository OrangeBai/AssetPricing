from config import *

from engine.basic import select_date, select_entity
from utils.dataframe import get_keys
from utils.date import *
from utils.path import concat_files, iter_files


def SplitData(file_name, split):
    """
    Split collected data into different files according to years
    :param file_name: 'Ret' or 'Ind'
    :param split: 'Daily', 'Weekly' or 'Monthly'
    :return:
    """
    if file_name == 'Ret':
        stk_key, date_key = get_keys('Ret')
    elif file_name == 'Ind':
        stk_key, date_key = get_keys('Ind')
    else:
        raise NameError('No data filed named {0}'.format(file_name))

    if split == 'Daily':
        path = os.path.join(RAW_DATA, file_name, 'Daily')
    elif split == 'Weekly':
        path = os.path.join(RAW_DATA, file_name, 'Weekly')
        date_key = 'Trdwnt'
    else:
        raise NameError('No data filed named {0}'.format(split))

    data_collection = {}
    year_tags = get_year_tags()

    csv_files = iter_files(path, 'csv')
    csv_data = concat_files(csv_files, converters={stk_key: str}, encoding='utf-8')

    for idx, year in enumerate(year_tags):
        data_collection[year] = select_date(csv_data, date_key, [year_tags[idx], year_tags[idx + 1]])
    for key, value in data_collection.items():
        value.to_csv(os.path.join(path, key + '.csv'), encoding='utf-8')
    return


def arrange_daily_data(file_name):
    if file_name == 'Ret':
        data_fields = ['Dsmvosd', 'Dsmvtll', 'Dretwd', 'Dretnd', 'Dnvaltrd']
        data_dir = os.path.join(RAW_DATA, file_name, 'Daily')
        arrange_dir = os.path.join(ARR_DATA, file_name, 'Daily')
        stk_key, date_key = get_keys('Ret')
    elif file_name == 'Ind':
        data_fields = ['PE', 'PB', 'Turnover', 'Liquidility']
        data_dir = os.path.join(RAW_DATA, file_name, 'Daily')
        arrange_dir = os.path.join(ARR_DATA, file_name, 'Daily')
        stk_key, date_key = get_keys('Ind')
    else:
        raise NameError('No data filed named {0}'.format(file_name))

    if not os.path.exists(arrange_dir):
        os.makedirs(arrange_dir)

    csv_files = iter_files(data_dir, 'csv')
    df = concat_files(csv_files, converters={stk_key: str}, encoding='utf-8')

    for data_field in data_fields:
        result = select_entity(df, [date_key, stk_key], df[stk_key].unique(), data_field)
        result.to_csv(os.path.join(arrange_dir, data_field + '.csv'), encoding='gbk')
    return


def convert_encoding(folder, StkFiled, decoding='gbk', encoding='utf-8'):
    files = iter_files(folder, 'csv')
    for file in files:
        df = pd.read_csv(file, encoding=decoding, converters={StkFiled: str})
        df.to_csv(file, encoding=encoding)
    return


if __name__ == '__main__':
    SplitData('Ind', 'Daily')
    SplitData('Ret', 'Daily')
    SplitData('Ret', 'Weekly')
    # arrange_daily_data('Ind')
    # arrange_daily_data('Ret')
