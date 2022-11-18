
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

source_folder_path = data_folder + 'trips/analysis/remove_outliers/'
destination_folder_path = data_folder + 'trips/analysis/remove_outliers/'

trips = pd.read_csv(source_folder_path + 'trips_grouped_by_day.csv')
first = time.time()
print('Read csv completed. Time = {time}'.format(time = first - start))

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['date'])
trips = dp.transform_to_time_series(trips, 'date')

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
