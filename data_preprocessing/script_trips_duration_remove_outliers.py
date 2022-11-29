import numpy as np
import pandas as pd
import sys
sys.path.append('../data_analysis')
sys.path.append('./data_analysis')
import os
import time
from modules.DataPreparation import DataPreparation

start = time.time()

if 'data_preprocessing' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/loaded_trips/'
destination_folder_path = data_folder + 'trips/preprocessing/'

second = time.time()
for year in ['2018', '2019', '2020', '2021', '2022']:
    trips = pd.read_csv(source_folder_path + 'trips_' + year + '.csv')
    first = second
    second = time.time()
    print('Read csv for year {year} completed. Time = {time}'.format(year = year,
                                                                    time = second - first))
    dp = DataPreparation()
    trips = dp.transform_to_datetime(trips, ['date'])
    trips = dp.transform_to_time_series(trips, 'date')
    trips_treated = trips.copy(deep=True)
    variable = 'tripduration'
    limit_outlier = 12*3600
    trips_treated[variable] = np.where(trips_treated[variable] > limit_outlier,
                                                np.nan, trips_treated[variable])
    number_outliers = len(trips[trips[variable] > limit_outlier])
    percentage_outliers = number_outliers/len(trips)
    print("For year = {year}, number of outliers = {number_outliers} and percentage = {percentage_outliers}".format(year = year,
                        number_outliers = number_outliers, percentage_outliers = percentage_outliers))
    trips_treated.to_csv(destination_folder_path + 'trips_' + year + '.csv')

end = time.time()

print('Time required to finish removing outliers from trip duration : {time}'.format(time = end - start))
