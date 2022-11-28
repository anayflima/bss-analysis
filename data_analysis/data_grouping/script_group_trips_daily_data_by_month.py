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

source_folder_path = data_folder + 'trips/analysis/remove_outliers/'
destination_folder_path = data_folder + 'trips/analysis/remove_outliers/'

trips = pd.read_csv(source_folder_path + 'trips_grouped_by_day.csv')

first = time.time()
print('Read csv completed. Time = {time}'.format(time = first - start))

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['date'])
trips = dp.transform_to_time_series(trips, 'date')

dg = DataGrouping(trips)

grouped_trips_day = trips

mean_grouped_trips_month, std_grouped_trips_month = dg.group_by_given_freq(grouped_trips_day, freq='MS')

third = time.time()
print('Group trips by month completed. Time = {time}'.format(time = third - first))

mean_grouped_trips_month.to_csv(destination_folder_path + 'trips_grouped_by_month_mean.csv')
std_grouped_trips_month.to_csv(destination_folder_path + 'trips_grouped_by_month_std.csv')

fourth = time.time()
print('Save to csv completed. Time = {time}'.format(time = fourth - third))

end = time.time()

print('Time to complete data grouping: {time}'.format(time = end - start))
