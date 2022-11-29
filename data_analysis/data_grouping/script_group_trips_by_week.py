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

# source_folder_path = data_folder + 'trips/loaded_trips/'
source_folder_path = data_folder + 'trips/preprocessed/'
# destination_folder_path = data_folder + 'trips/new_grouping/'
destination_folder_path = data_folder + 'trips/preprocessed/grouped/'

trips = pd.read_csv(source_folder_path + 'all_trips.csv')
# trips = pd.read_csv(source_folder_path + 'trips_test.csv')
first = time.time()
print('Read csv completed. Time = {time}'.format(time = first - start))

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['starttime', 'stoptime'])
trips = dp.transform_to_time_series(trips, 'starttime')
trips = dp.calculate_and_add_age_column(trips)

second = time.time()

dg = DataGrouping(trips)
mean_grouped_trips_month, std_grouped_trips_month = dg.group_by_given_freq(freq='W')


third = time.time()
print('Group trips by week completed. Time = {time}'.format(time = third - second))

mean_grouped_trips_month.to_csv(destination_folder_path + 'trips_grouped_by_week_mean.csv')
std_grouped_trips_month.to_csv(destination_folder_path + 'trips_grouped_by_week_std.csv')

fourth = time.time()
print('Save to csv completed. Time = {time}'.format(time = fourth - third))

end = time.time()

print('Time to complete data grouping: {time}'.format(time = end - start))
