import time
import pandas as pd
import sys
sys.path.append('./load_trips')
import os

if 'load_trips' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

start = time.time()


folder_path = data_folder + 'trips/loaded_trips/'

trips_2018 = pd.read_csv(folder_path + 'trips_2018.csv')
trips_2019 = pd.read_csv(folder_path + 'trips_2019.csv')
trips_2020 = pd.read_csv(folder_path + 'trips_2020.csv')
trips_2021 = pd.read_csv(folder_path + 'trips_2021.csv')
trips_2022 = pd.read_csv(folder_path + 'trips_2022.csv')

first = time.time()
print('Read csv completed. Time = {time}'.format(time = first - start))

trips = trips_2018.append(trips_2019)
trips = trips.append(trips_2020)
trips = trips.append(trips_2021)
trips = trips.append(trips_2022)

second = time.time()
print('Join trips completed. Time = {time}'.format(time = second - first))

# Make index unique

trips = trips.drop('Index', axis = 1)
trips.insert(0, 'Index', range(0,0 + len(trips)))

trips = trips.set_index('Index')

third = time.time()
print('Set index completed. Time = {time}'.format(time = third - second))

trips.to_csv(folder_path + 'all_trips.csv')

fourth = time.time()
print('Save to csv completed. Time = {time}'.format(time = fourth - third))

end = time.time()

print('Time to join all trips: {time}'.format(time = end - start))