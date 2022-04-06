import os
import pandas as pd

from utils.date import str_date_to_list


def check_ext(file_path, ext):
    """
    Compare file extension
    :param file_path: path of the file
    :param ext: extension name, e.g. 'csv', 'pdf'
    :return: True or False
    """
    return file_path.split('.')[-1] == ext


def concat_files(files, **kwargs):
    """
    given a list of file path, concat the dataframes into one and drop duplicates
    :param files: a list of files
    :param kwargs: keywords for loading the file
    :return: the dataframe
    """
    csv_data = pd.DataFrame()
    for file in files:
        csv_data = csv_data.append(pd.read_csv(file, **kwargs))
    csv_data = csv_data.drop_duplicates()
    return csv_data


def iter_files(base_dir, ext):
    """
    walk in the base directory and list all the files with given extension
    :param base_dir: the base directory
    :param ext: extension name
    :return: a list of file paths
    """
    all_files = []
    for root, folder, files in os.walk(base_dir):
        for file in files:
            if check_ext(file, ext):
                all_files += [os.path.join(root, file)]
    return all_files


def select_daily_files(data_dir, period):
    """
    Select csv files that contains all the data in period
    :param data_dir: directory of csv files
    :param period: [start_date(include), end_data(exclude)]
    :return: csv_files
    """
    csv_files = [file for file in os.listdir(data_dir) if check_ext(file, 'csv')]
    start_year, end_year = str_date_to_list(period[0])[0], str_date_to_list(period[1])[0]
    for file in csv_files:
        file_year = int(file.split('.')[0])
        if file_year < start_year or file_year > end_year:
            csv_files.remove(file)
    return [os.path.join(data_dir, file) for file in csv_files]
