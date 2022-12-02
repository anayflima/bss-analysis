
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
destination_folder_path = data_folder + 'trips/preprocessed/'

trips = pd.read_csv(source_folder_path + 'all_trips.csv')
# trips = pd.read_csv(source_folder_path + 'trips_few.csv')
first = time.time()
print('Read csv completed. Time = {time}'.format(time = first - start))

dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['starttime', 'stoptime'])
trips = dp.transform_to_time_series(trips, 'starttime')

trips_before_covid = trips[:os.environ['LAST_DAY_BEFORE_COVID']]
trips_before_covid.to_csv(destination_folder_path + 'trips_before_covid.csv')

second = time.time()
print('Before covid: Save to csv completed. Time = {time}'.format(time = second - first))

trips_during_covid = trips[os.environ['FIRST_DAY_COVID']:]
trips_during_covid.to_csv(destination_folder_path + 'trips_during_covid.csv')

third = time.time()
print('During covid: Save to csv completed. Time = {time}'.format(time = third - second))

end = time.time()

print('Time to complete trips separation: {time}'.format(time = end - start))
