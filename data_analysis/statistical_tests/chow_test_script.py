from bokeh.plotting import figure, output_file, show
from bokeh.models import LinearAxis, Range1d
import pandas as pd

import pandas as pd
import numpy as np
import os
import sys
sys.path.append('./data_analysis')

if 'statistical_tests' in os.getcwd():
    data_folder = './../../data/'
elif 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/analysis/'
destination_folder_path = data_folder + 'charts/'
covid_data = pd.read_csv(data_folder + 'covid/treated_data/data.csv')

trips = pd.read_csv(source_folder_path + 'trips_grouped_by_month_mean.csv')

from modules.DataPreparation import DataPreparation
dp = DataPreparation()

covid_data = dp.transform_to_datetime(covid_data, ['date'])
covid_data = dp.transform_to_time_series(covid_data, 'date', drop=True)

trips = dp.transform_to_datetime(trips, ['date'])
trips = dp.transform_to_time_series(trips, 'date', drop = False)

from chowtest import ChowTest

results = ChowTest(y=pd.Series(trips['tripduration']),
            X=pd.Series([trips['date']]),
            last_index_in_model_1='2020-09-01',
            first_index_in_model_2='2020-10-01')

print(results)