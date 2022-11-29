import pandas as pd
import pandas_bokeh
import sys
sys.path.append('./data_analysis')
sys.path.append('../../data_analysis')
import os

from modules.DataPreparation import DataPreparation

if 'bokeh_plot' in os.getcwd():
    data_folder = '../../data/'
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
trips = dp.transform_to_time_series(trips, 'date', drop = True)

trips_and_covid = pd.merge(trips, covid_data, left_index=True,
                            right_index=True, how = 'left')

trips_and_covid['date_trips'] = trips_and_covid.index

variable = 'age'

pandas_bokeh.output_file(destination_folder_path + 'monthly_'+ variable + '.html')

trips_and_covid.plot_bokeh(
    kind='line',
    figsize=(900, 400),
    sizing_mode="scale_width",
    # rangetool=True,
    x='date_trips',
    # y=['number_of_trips', 'tripduration', 'new_cases_ma'],
    y=[variable],
    # dropdown=["number_of_trips", "tripduration"],
    xlabel='Variable',
    ylabel='Date',
    title='Trips variable from 2018 to 2022',
)