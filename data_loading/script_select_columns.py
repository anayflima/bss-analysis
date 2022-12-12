
import pandas as pd
import sys
sys.path.append('./data_analysis')
import os
import time
from modules.DataPreparation import DataPreparation

from dotenv import load_dotenv

load_dotenv()

start = time.time()

if 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/preprocessed/'
destination_folder_path = data_folder + 'trips/selected_columns/'

# trips = pd.read_csv(source_folder_path + 'all_trips.csv')
filename = 'all_trips.csv'
filename = 'trips_few.csv'

second = time.time()

# for filename in ['all_trips.csv', 'trips_2018.csv', 'trips_2019.csv',
#                  'trips_2020.csv', 'trips_2021.csv', 'trips_2022.csv']:
for filename in ['trips_2021.csv', 'trips_2022.csv']:

    trips = pd.read_csv(source_folder_path + filename)
    first = second

    trips = trips.filter(['date', 'lat_start', 'lon_start', 'lat_end', 
                        'lon_end', 'tripduration', 'starttime', 'stoptime',
                        'age', 'distance', 'weekend', 'holiday'])

    trips.to_csv(destination_folder_path + filename, index=False)

    second = time.time()
    print('{filename} completed. Time = {time}'.format(filename = filename, 
                                                        time = second - first))

end = time.time()

print('Time to complete selection of columns: {time}'.format(time = end - start))
