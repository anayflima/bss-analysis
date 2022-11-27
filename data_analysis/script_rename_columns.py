
import pandas as pd
import sys
sys.path.append('./data_analysis')
import os
import time

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

trips = trips.rename({'distance_in_meters_bicycle':'distance'}, axis = 1)

trips.to_csv(destination_folder_path + 'all_trips.csv')