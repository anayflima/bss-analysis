import pandas as pd
import sys
sys.path.append('./data_analysis')
import os

from modules.DataPreparation import DataPreparation
from modules.DataGrouping import DataGrouping

import time

if 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/loaded_trips/'
# source_folder_path = data_folder + 'trips/test/loaded_trips/'
destination_folder_path = data_folder + 'trips/loaded_trips/'
# destination_folder_path = data_folder + 'trips/test/analysis/'

now = time.time()

all_trips = pd.read_csv(source_folder_path + 'all_trips.csv')
dp = DataPreparation()
all_trips = dp.transform_to_datetime(all_trips, ['starttime', 'stoptime'])
all_trips = dp.transform_to_time_series(all_trips, 'starttime')

for year in ['2018', '2019', '2020', '2021', '2022']:
    anterior = now
    now = time.time()
    trips = all_trips[year:year]
    trips = dp.calculate_and_add_age_column(trips)
    trips.to_csv(destination_folder_path + 'trips_'+year+'.csv')
    print('{year} completed. Time = {time}'.format(year = year, time = now - anterior))