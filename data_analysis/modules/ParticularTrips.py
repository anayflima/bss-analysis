import pandas as pd
import numpy as np
import sys
sys.path.append('./data_analysis')
sys.path.append('../../data_analysis')
from modules.DataPreparation import DataPreparation
import matplotlib.pyplot as plt
from  matplotlib.ticker import FuncFormatter
from matplotlib.pyplot import figure
import seaborn as sns

class ParticularTrips:
    def __init__(self, data_folder = '', period_covid = 'all'):
        self.data_folder = data_folder
        self.period_covid = period_covid
        self.particular_trips = {}
        self.percentage = {}
    
    def import_and_prepare_trips_data(self,
            file_path = 'trips/preprocessed/trips_{period_covid}_covid.csv'):
        if '{period_covid}' in file_path:
            file_path = file_path.format(period_covid = self.period_covid)
        trips = pd.read_csv(self.data_folder + file_path)  
        dp = DataPreparation()
        trips = dp.transform_to_datetime(trips, ['date'])
        trips = dp.transform_to_time_series(trips, 'date', drop = True)
        self.trips = trips
    
    def set_trips(self, trips):
        self.trips = trips
    
    def get_weekend_trips(self, trips):
        return trips[trips['weekend']]
    
    def get_weekday_trips(self, trips):
        return trips[~trips['weekend']]
    
    def get_circular_trips(self, trips):
        return trips[trips['distance'] == 0]
    
    def get_non_circular_trips(self, trips):
        return trips[trips['distance'] != 0]
    
    def return_particular_trips_of_type(self, trips, trips_type):
        if trips_type == 'weekend':
            return self.get_weekend_trips(trips)
        elif trips_type == 'weekday':
            return self.get_weekday_trips(trips)
        elif trips_type == 'circular':
            return self.get_circular_trips(trips)
        elif trips_type == 'non-circular':
            return self.get_non_circular_trips(trips)
        else:
            return -1
    
    def get_particular_trips(self):
        self.particular_trips['weekend'] = self.get_weekend_trips(self.trips)
        self.particular_trips['weekday'] = self.get_weekday_trips(self.trips)
        self.particular_trips['circular'] = self.get_circular_trips(self.trips)
        self.particular_trips['non-circular'] = self.get_non_circular_trips(self.trips)
    
    # def calculate_percentage_particular_trips(self, type_trips):
    #     percentage = len(self.particular_trips[type_trips])/len(self.trips)
    #     print('The percentage of {type_trips} trips {period_covid} COVID is {percentage}'.format(
    #         type_trips = type_trips,
    #         period_covid = self.period_covid,
    #         percentage = percentage
    #     ))
    #     self.percentage[type_trips] = percentage
    
    def calculate_percentage_particular_trips(self, type_trips_numerator,
                                                type_trips_denominator = ''):
        
        if type_trips_denominator == '':
            trips_denominator = self.trips
        else:
            trips_denominator = self.particular_trips[type_trips_denominator]
        
        if trips_denominator.empty:
            print("There is no trip with the type_trips_denominator specified")
            return None

        # We want the percentage of the numerator type of trips
        # in another group of trips (trips_denominator)
        trips_numerator = self.return_particular_trips_of_type(trips_denominator, type_trips_numerator)
        
        if not isinstance(trips_numerator, pd.DataFrame) and trips_numerator == -1:
            print("Invalid trip type for numerator")
            return None

        percentage = len(trips_numerator)/len(trips_denominator)

        if type_trips_denominator == '':
            print_message = 'The percentage of {type_trips_numerator} trips ' \
                            + '{period_covid} COVID is {percentage}'
            print(print_message.format(
                type_trips_numerator = type_trips_numerator,
                period_covid = self.period_covid,
                percentage = percentage
            ))
            key_dictionary_percentage = type_trips_numerator
        else:
            print_message = 'The percentage of {type_trips_numerator} trips inside the ' \
              + '{type_trips_denominator} trips {period_covid} COVID is {percentage}'
            print(print_message.format(
                type_trips_numerator = type_trips_numerator,
                type_trips_denominator = type_trips_denominator,
                period_covid = self.period_covid,
                percentage = percentage
            ))
            key_dictionary_percentage = type_trips_numerator + '_over_' + type_trips_denominator
        
        self.percentage[key_dictionary_percentage] = percentage
    
    def calculate_all_percentages(self):
        self.get_particular_trips()

        self.calculate_percentage_particular_trips('weekend')
        self.calculate_percentage_particular_trips('weekday')
        self.calculate_percentage_particular_trips('circular')
        self.calculate_percentage_particular_trips('non-circular')

        print()

        self.calculate_percentage_particular_trips('circular', 'weekend')
        self.calculate_percentage_particular_trips('circular', 'weekday')
        self.calculate_percentage_particular_trips('weekend', 'circular')
        self.calculate_percentage_particular_trips('weekday', 'circular')

    def plot_histogram_trip_duration(self):
        limit_bins_hours = 6
        limit_bins_seconds = 3600*limit_bins_hours+1
        step_seconds = 60*20
        variable = 'tripduration'

        # from 0 to 12 hours (3600*12 seconds), with step of 20 minutes
        bins = list(range(0,limit_bins_seconds,step_seconds))

        sns.set(rc={'figure.figsize':(20,11)})
        ax = sns.histplot(data=self.trips[variable], bins = bins, stat='percent')
        for i in ax.containers:
            ax.bar_label(i,fmt='%.1f')
        
        # tickers for every 20 minutes
        ax.set_xticks(range(0,limit_bins_seconds,step_seconds))
        figure(figsize=(12, 6), dpi=80)

        # show y axis labels in minutes, rather than in seconds
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: x//60))

        ax.set_ylim(bottom = 0, top = 70)

        ax.set(xlabel='Trip duration (min)', ylabel='Percent of trips (%)')
        ax.set(title='Trip duration distribution')

        # if period != 'all' and day != '':
        # ax.set(title='Trip duration distribution ' + period + ' covid' + ' for ' + day)
        # else:
        #     ax.set(title='Trip duration distribution')
        # # plt.figure(figsize=(20,6))
        # plt.savefig(data_folder + 'charts/histograms/all_trips_tripduration_'+ day+'_' +period+'_covid.png')
    
    def plot_histogram(self, variable):
        if variable == 'tripduration':
            self.plot_histogram_trip_duration()
