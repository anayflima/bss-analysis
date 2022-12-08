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

source_folder_path = 'trips/preprocessed/'
destination_folder_path = data_folder + 'trips/analysis_results/'
file_path = source_folder_path + 'all_trips.csv'
# file_path = source_folder_path + 'trips_before_covid_test.csv'

pt = ParticularTrips(data_folder)
pt.import_and_prepare_trips_data(file_path=file_path)

first = time.time()
print('Import and prepare data completed. Time = {time}'.format(time = first - start))

circular_trips = pt.get_circular_trips(pt.trips)
print('circular_trips')
print(circular_trips.head())

end = time.time()

circular_trips.to_csv(destination_folder_path + 'circular_trips.csv', index=False)
print('Circular trips selection completed. Time = {time}'.format(time = end - start))