import os
import sys
sys.path.append('./')
sys.path.append('./data_loading')
from modules.TripsLoading import TripsLoading
sys.path.append('./data_analysis')
from modules.DataPreparation import DataPreparation
sys.path.append('./stations_treatment')
from modules.TripStationsTreatment import TripStationsTreatment

import time
start = time.time()

if 'data_loading' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/treated_data/'
destination_folder_path = data_folder + 'trips/loaded_trips/'

'''
Load only files that follow a specific name pattern:
'''
file_filter = source_folder_path + 'trips_BikeSampa_*.csv'
# file_filter = source_folder_path + 'trips_BikeSampa_2022*.csv'

tl = TripsLoading()
trips = tl.load_trips_files(file_filter)

first = time.time()
print('Time to complete loading trips files: {time}'.format(time = first - start))

tst = TripStationsTreatment()

trips = tst.find_station_ids_and_add_columns(trips)
trips = tst.find_station_names_and_add_columns(trips)
trips = tst.find_station_coordinates_and_add_columns(trips)
trips = tst.find_trip_distance_and_add_column(trips)

second = time.time()

print('Time to complete adding columns: {time}'.format(time = second - first))

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['starttime', 'stoptime'])
trips = dp.transform_to_time_series(trips, 'starttime')

print(list(trips.columns))

assert set(list(trips.columns)) == set(['tripduration', 'start_station_name_old',
       'start_station_id', 'starttime', 'end_station_name_old', 'end_station_id',
       'stoptime', 'birth_year', 'age', 'per_day', 'hour', 'week_day',
       'weekend', 'holiday','start_station_name','end_station_name',
       'lat_start', 'lon_start','lat_end', 'lon_end', 'distance'])

trips.to_csv(destination_folder_path + 'all_trips.csv')
# trips.to_csv(destination_folder_path + 'trips_2022.csv')

end = time.time()

print('Time to complete all trips data loading: {time}'.format(time = end - start))