
import pandas as pd
import sys
sys.path.append('./data_analysis')
import os
import time
from modules.DataPreparation import DataPreparation

start = time.time()

if 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/loaded_trips/'
destination_folder_path = data_folder + 'trips/loaded_trips/'

trips = pd.read_csv(source_folder_path + 'all_trips.csv')
first = time.time()
print('Read csv completed. Time = {time}'.format(time = first - start))

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['starttime', 'stoptime'])
trips = dp.transform_to_time_series(trips, 'starttime')

trips_before_covid = trips[:'2020-3-05']
trips_before_covid.to_csv(destination_folder_path + 'trips_before_covid.csv')

second = time.time()
print('Before covid: Save to csv completed. Time = {time}'.format(time = second - first))

trips_after_covid = trips['2020-3-06':]
trips_after_covid.to_csv(destination_folder_path + 'trips_after_covid.csv')

third = time.time()
print('After covid: Save to csv completed. Time = {time}'.format(time = third - second))

end = time.time()

print('Time to complete trips separation: {time}'.format(time = end - start))
