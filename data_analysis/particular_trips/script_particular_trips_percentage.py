
import pandas as pd
import sys
sys.path.append('./data_analysis')
sys.path.append('../../data_analysis')
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
destination_folder_path = data_folder + 'trips/analysis_results/percentage_particular_trips/'
file_path = source_folder_path + 'all_trips.csv'

pt = ParticularTrips(data_folder = data_folder,
                     destination_folder = destination_folder_path)

pt.import_and_prepare_trips_data(file_path=file_path)

first = time.time()
print('Data preparation completed. Time = {time}'.format(time = first - start))

pt.calculate_monthly_percentage(print=False)

second = time.time()

print('Monthly percentages calculation completed. Time = {time}'.format(time = second - first))

print('Percentage of particular trips completed. Time = {time}'.format(time = second - start))