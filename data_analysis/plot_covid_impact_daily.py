import pandas as pd
import numpy as np
import pandas_bokeh
from bokeh.models import LinearAxis, Range1d
import os
import sys
sys.path.append('./data_analysis')

if 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/analysis/'
destination_folder_path = data_folder + 'charts/'

trips = pd.read_csv(source_folder_path + 'trips_grouped_by_day.csv')

from modules.DataPreparation import DataPreparation
dp = DataPreparation()
trips = dp.transform_to_datetime(trips, ['date'])
trips = dp.transform_to_time_series(trips, 'date', drop = True)
trips['date_trips'] = trips.index

pandas_bokeh.output_file(destination_folder_path + 'daily.html')



trips.plot_bokeh(
    kind='line',
    x='date_trips',
    y=['number_of_trips', 'tripduration', 'age'],
    extra_y_range={
        'age_range': Range1d(
        start=trips['age'].min(),
        end=trips['age'].max(),
    )},
    xlabel='Variable',
    ylabel='Date',
    title='Trips variable from 2018 to 2022'
)