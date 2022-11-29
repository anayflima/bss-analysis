from bokeh.plotting import figure, output_file, show
from bokeh.models import LinearAxis, Range1d
import pandas as pd

import pandas as pd
import numpy as np
import pandas_bokeh
import os
import sys
sys.path.append('./data_analysis')

if 'data_analysis' in os.getcwd():
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

# pandas dataframe
x_column = "date_trips"
y_column1 = "number_of_trips"
y_column2 = "new_cases_ma"

pandas_bokeh.output_file(destination_folder_path + 'monthly_covid'+
                            y_column2 + '_'+ y_column1 +'.html')

# Bokeh plot
output_file("twin_axis.html")

y_overlimit = 0.05 # show y axis below and above y min and max value
p = figure()

# FIRST AXIS
p.line(trips_and_covid[x_column], trips_and_covid[y_column1],
        legend=y_column1, line_width=1, color="blue")

p.y_range = Range1d(
    trips_and_covid[y_column1].min() * (1 - y_overlimit),
    trips_and_covid[y_column1].max() * (1 + y_overlimit)
)

# SECOND AXIS
y_column2_range = y_column2 + "_range"
p.extra_y_ranges = {
    y_column2_range: Range1d(
        start=trips_and_covid[y_column2].min() * (1 - y_overlimit),
        end=trips_and_covid[y_column2].max() * (1 + y_overlimit),
    )
}
p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

p.line(
    trips_and_covid[x_column],
    trips_and_covid[y_column2],
    legend=y_column2,
    line_width=1,
    y_range_name=y_column2_range,
    color="green"
)

show(p)