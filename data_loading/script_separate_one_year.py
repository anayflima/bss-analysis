import pandas as pd
import sys
sys.path.append('./data_analysis')
sys.path.append('../data_analysis')
import os

from modules.DataPreparation import DataPreparation
from modules.DataGrouping import DataGrouping

import time

start = time.time()

if 'data_loading' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/loaded_trips/'
# source_folder_path = data_folder + 'trips/preprocessing/'
# destination_folder_path = data_folder + 'trips/new_grouping/'
destination_folder_path = data_folder + 'trips/loaded_trips/'

trips = pd.read_csv(source_folder_path + 'all_trips.csv')
first = time.time()
print('Read csv completed. Time = {time}'.format(time = first - start))

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['starttime', 'stoptime'])
trips = dp.transform_to_time_series(trips, 'starttime')
trips = dp.calculate_and_add_age_column(trips)

trips_2019 = trips['2019']

trips_2019.to_csv(destination_folder_path + 'trips_2019.csv')
