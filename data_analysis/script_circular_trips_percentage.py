
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

for year in ['2018','2019','2020','2021','2022']:
# for year in ['2018']:
    for month in range(1,13):
        print(year+'-'+str(month)+':'+year+'-'+ str(month))
        trips_month = trips[year+'-'+str(month):year+'-'+ str(month)]
        if len(trips_month) > 0:
            ct = CircularTrips()
            trips_month = ct.convert_distance_to_int(trips_month)
            percentage = ct.calculate_percentage_of_circular_trips(trips_month)
            print('percentage')
            print(percentage)
            df_percentages = df_percentages.append({'date': year+'-'+str(month), 'percentage': percentage}, ignore_index=True)
            print(df_percentages)

df_percentages.to_csv(destination_folder_path + 'circular_trips_percentage.csv', index=False)