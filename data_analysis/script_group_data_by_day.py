import pandas as pd
import sys
sys.path.append('./data_analysis')
import os

from modules.DataPreparation import DataPreparation
from modules.DataGrouping import DataGrouping

import time

start = time.time()

if 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/loaded_trips/'
destination_folder_path = data_folder + 'trips/analysis/'

trips = pd.read_csv(source_folder_path + 'all_trips.csv')
first = time.time()
print('Read csv completed. Time = {time}'.format(time = first - start))

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['starttime', 'stoptime'])
trips = dp.transform_to_time_series(trips, 'starttime')
trips = dp.calculate_and_add_age_column(trips)

dg = DataGrouping(trips)
grouped_trips = dg.group_all_trips_data()

second = time.time()
print('Group trips completed. Time = {time}'.format(time = second - first))

grouped_trips.to_csv(destination_folder_path + 'trips_grouped_by_day.csv')

third = time.time()
print('Save to csv completed. Time = {time}'.format(time = third - second))

end = time.time()

print('Time to complete data grouping: {time}'.format(time = end - start))
