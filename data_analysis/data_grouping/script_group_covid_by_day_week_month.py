import pandas as pd
import sys
sys.path.append('./data_analysis')
sys.path.append('../../data_analysis')
import os

from modules.DataPreparation import DataPreparation
from modules.DataGrouping import DataGrouping

import time

start = time.time()

if 'data_grouping' in os.getcwd():
    data_folder = '../../data/'
elif 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'covid/treated_data/'
destination_folder_path = data_folder + 'covid/grouped/'

covid_data = pd.read_csv(source_folder_path + '/data.csv')

dp = DataPreparation()

covid_data = dp.transform_to_datetime(covid_data, ['date'])
covid_data = dp.transform_to_time_series(covid_data, 'date', drop=True)

dg = DataGrouping(covid_data)

mean_grouped_trips_day, std_grouped_trips_day = dg.group_by_given_freq(freq='D', covid = True)
mean_grouped_trips_day.to_csv(destination_folder_path + 'covid_grouped_by_day_mean.csv')
std_grouped_trips_day.to_csv(destination_folder_path + 'covid_grouped_by_day_std.csv')

mean_grouped_trips_week, std_grouped_trips_week = dg.group_by_given_freq(freq='W', covid = True)
mean_grouped_trips_week.to_csv(destination_folder_path + 'covid_grouped_by_week_mean.csv')
std_grouped_trips_week.to_csv(destination_folder_path + 'covid_grouped_by_week_std.csv')

mean_grouped_trips_month, std_grouped_trips_month = dg.group_by_given_freq(freq='MS', covid = True)
mean_grouped_trips_month.to_csv(destination_folder_path + 'covid_grouped_by_month_mean.csv')
std_grouped_trips_month.to_csv(destination_folder_path + 'covid_grouped_by_month_std.csv')