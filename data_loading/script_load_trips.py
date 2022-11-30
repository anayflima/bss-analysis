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

# year = '2022'

# file_filter = source_folder_path + 'trips_BikeSampa_' + year + '*.csv'
file_filter = source_folder_path + 'trips_BikeSampa_*.csv'

tl = TripsLoading()
trips = tl.load_trips_files(file_filter)

tst = TripStationsTreatment()

trips = tst.find_station_ids_and_add_columns(trips)
trips = tst.find_station_names_and_add_columns(trips)

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['starttime', 'stoptime'])
trips = dp.transform_to_time_series(trips, 'starttime')

print(list(trips.columns))

assert list(trips.columns) == ['tripduration', 'start_station_name_old',
       'start_station_id', 'starttime', 'end_station_name_old', 'end_station_id',
       'stoptime', 'birth_year', 'age', 'per_day', 'hour', 'week_day',
       'weekend', 'holiday','start_station_name','end_station_name']

# trips.to_csv(destination_folder_path + 'trips_' + year + '.csv')
trips.to_csv(destination_folder_path + 'all_trips.csv')

end = time.time()

# print('Time to complete trips data loading for year {year}: {time}'.format(year = year, time = end - start))
print('Time to complete all trips data loading: {time}'.format(time = end - start))