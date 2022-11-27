
import pandas as pd
import sys
sys.path.append('./data_analysis')
import os
import time
from modules.DataPreparation import DataPreparation
from modules.CircularTrips import CircularTrips

start = time.time()

if 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/loaded_trips/'
destination_folder_path = data_folder + 'trips/analysis_results/'

trips = pd.read_csv(source_folder_path + 'all_trips.csv')
# trips = pd.read_csv(source_folder_path + 'trips_few.csv')
# trips = pd.read_csv(source_folder_path + 'trips_2018.csv')
first = time.time()
print('Read csv completed. Time = {time}'.format(time = first - start))
print(trips.columns)

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['starttime', 'stoptime'])
trips = dp.transform_to_time_series(trips, 'starttime')
second = time.time()
print('Transform to time series completed. Time = {time}'.format(time = second - first))

df_percentages = pd.DataFrame(columns = ['date', 'percentage'], dtype=object)


ct = CircularTrips()
trips = ct.convert_distance_to_int(trips)
circular_trips = ct.find_circular_trips(trips)
print('circular_trips')
print(circular_trips.head())

circular_trips.to_csv(destination_folder_path + 'circular_trips.csv', index=False)