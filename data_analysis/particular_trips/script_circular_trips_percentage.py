
import pandas as pd
import sys
sys.path.append('./data_analysis')
sys.path.append('../../data_analysis')
from modules.DataPreparation import DataPreparation
from modules.ParticularTrips import ParticularTrips

import os

if 'circular_trips' in os.getcwd():
    data_folder = '../../data/'
elif 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

import time
start = time.time()

source_folder_path = data_folder + 'trips/preprocessed/'
destination_folder_path = data_folder + 'trips/analysis_results/'

trips = pd.read_csv(source_folder_path + 'all_trips.csv')

first = time.time()
print('Read csv completed. Time = {time}'.format(time = first - start))

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['starttime', 'stoptime'])
trips = dp.transform_to_time_series(trips, 'starttime')
second = time.time()
print('Transform to time series completed. Time = {time}'.format(time = second - first))

df_percentages = pd.DataFrame(columns = ['date', 'percentage'], dtype=object)

for year in ['2018','2019','2020','2021','2022']:
    for month in range(1,13):
        trips_month = trips[year+'-'+str(month):year+'-'+ str(month)]
        if len(trips_month) > 0:
            pt = ParticularTrips()
            pt.set_trips(trips_month)
            pt.calculate_percentage_particular_trips('circular')
            percentage = pt.percentage['circular']
            df_percentages = df_percentages.append({'date': year+'-'+str(month), 'percentage': percentage}, ignore_index=True)

df_percentages.to_csv(destination_folder_path + 'circular_trips_percentage_other.csv', index=False)