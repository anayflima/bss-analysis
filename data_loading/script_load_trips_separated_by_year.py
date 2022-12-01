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

second = time.time()

for year in ['2018', '2019', '2020', '2021', '2022']:

    file_filter = source_folder_path + 'trips_BikeSampa_' + year + '*.csv'

    tl = TripsLoading()
    trips = tl.load_trips_files(file_filter)

    tst = TripStationsTreatment()

    trips = tst.find_station_ids_and_add_columns(trips)
    trips = tst.find_station_names_and_add_columns(trips)
    trips = tst.find_trip_distance_and_add_column(trips)

    dp = DataPreparation()
    trips = dp.transform_to_datetime(trips, ['starttime', 'stoptime'])
    trips = dp.transform_to_time_series(trips, 'starttime')

    print(list(trips.columns))

    assert list(trips.columns) == ['tripduration', 'start_station_name_old',
        'start_station_id', 'starttime', 'end_station_name_old', 'end_station_id',
        'stoptime', 'birth_year', 'age', 'per_day', 'hour', 'week_day',
        'weekend', 'holiday','start_station_name','end_station_name', 'distance']

    trips.to_csv(destination_folder_path + 'trips_' + year + '.csv')

    first = second
    second = time.time()
    print('Time to complete trips data loading for year {year}: {time}'.format(year = year, time = second - first))

end = time.time()

print('Time to complete trips data loading, separated by year: {time}'.format(time = end - start))