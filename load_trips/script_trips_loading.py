import os
import sys
sys.path.append('./load_trips')
sys.path.append('../')
import tembici.load_trips as lt
import time

start = time.time()

if 'load_trips' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/test/original_data/'
destination_folder_path = data_folder + 'trips/test/treated_data/'

file_filter = source_folder_path + '*.csv'

# tl = TripsLoading()
# trips = tl.load_trips_files(file_filter)

trips = lt.load_trips_files(file_filter)
trips.to_csv(destination_folder_path + 'trips.csv')

end = time.time()

print('Time to complete trip data loading: {time}'.format(time = end - start))