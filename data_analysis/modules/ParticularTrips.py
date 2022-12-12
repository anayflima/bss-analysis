import pandas as pd
import numpy as np
import sys
sys.path.append('./data_analysis')
sys.path.append('../../data_analysis')
from modules.DataPreparation import DataPreparation
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from  matplotlib.ticker import FuncFormatter
from matplotlib.pyplot import figure
import seaborn as sns

class ParticularTrips:
    def __init__(self, data_folder = '', period_covid = '',
                 destination_folder = './data/trips/analysis_results/'):
        self.data_folder = data_folder
        self.period_covid = period_covid
        self.destination_folder = destination_folder
        self.particular_trips = {}
        self.percentage = {}
        self.types_trips = ['long','weekend', 'weekday', 'circular', 'non_circular',
                            'holiday', 'working_days', 'non_working_days',
                            'morning', 'lunchtime', 'afternoon', 'evening']
    
    def import_and_prepare_trips_data(self,
            file_path = 'trips/preprocessed/trips_{period_covid}_covid.csv'):
        if '{period_covid}' in file_path:
            if self.period_covid == 'all':
                file_path = 'trips/preprocessed/all_trips.csv'
            else:
                file_path = file_path.format(period_covid = self.period_covid)
        print('read_csv')
        trips = pd.read_csv(self.data_folder + file_path)
        dp = DataPreparation()
        print('transform_to_datetime')
        trips = dp.transform_to_datetime(trips, ['date'])
        print('transform_to_time_series')
        trips = dp.transform_to_time_series(trips, 'date', drop = True)
        self.trips = trips
    
    def set_trips(self, trips):
        self.trips = trips
    
    def get_long_trips(self, trips):
        return trips[trips['tripduration'] >= 80*60]
    
    def get_short_trips(self, trips):
        return trips[trips['tripduration'] < 80*60]
    
    def get_circular_trips(self, trips):
        return trips[trips['distance'] == 0]
    
    def get_non_circular_trips(self, trips):
        return trips[trips['distance'] != 0]

    def get_weekend_trips(self, trips):
        return trips[trips['weekend']]
    
    def get_weekday_trips(self, trips):
        return trips[~trips['weekend']]

    def get_holiday_trips(self, trips):
        """Filter the holiday trips, returning a new dataframe."""
        return trips[trips['holiday']]
    
    def get_working_days_trips(self, trips):
        """Filter the working days trips, returning a new dataframe."""
        return trips[~trips['weekend'] & ~trips['holiday']]

    def get_non_working_days_trips(self, trips):
        """Filter the weekend+holiday trips, returning a new dataframe."""
        return trips[trips['weekend'] | trips['holiday']]
        
    def get_morning_trips(self, trips):
        """
            Filter the morning trips, returning a new dataframe.
            From 6:00 - 8:59
        """
        return trips[(trips['hour'] >= 6)  & (trips['hour'] <= 8)]

    def get_lunchtime_trips(self, trips):
        """
            Filter the lunchtime trips, returning a new dataframe.
            From 11:00 - 13:59
        """
        return trips[(trips['hour'] >= 11)  & (trips['hour'] <= 13)]

    def get_afternoon_trips(self, trips):
        """
            Filter the afternoon trips, returning a new dataframe.
            From 14:00 - 16:59
        """
        return trips[(trips['hour'] >= 14)  & (trips['hour'] <= 16)]
    
    def get_evening_trips(self, trips):
        """
            Filter the evening trips, returning a new dataframe.
            From 17:00 - 18:59
        """
        return trips[(trips['hour'] >= 17)  & (trips['hour'] <= 18)]
    
    def return_particular_trips_of_type(self, trips, trips_type):
        if trips_type == 'circular':
            return self.get_circular_trips(trips)
        elif trips_type == 'non_circular':
            return self.get_non_circular_trips(trips)
        elif trips_type == 'weekend':
            return self.get_weekend_trips(trips)
        elif trips_type == 'weekday':
            return self.get_weekday_trips(trips)
        elif trips_type == 'holiday':
            return self.get_holiday_trips(trips)
        elif trips_type == 'working_days':
            return self.get_working_days_trips(trips)
        elif trips_type == 'non_working_days':
            return self.get_non_working_days_trips(trips)
        elif trips_type == 'morning':
            return self.get_morning_trips(trips)
        elif trips_type == 'lunchtime':
            return self.get_lunchtime_trips(trips)
        elif trips_type == 'afternoon':
            return self.get_afternoon_trips(trips)
        elif trips_type == 'evening':
            return self.get_evening_trips(trips)
        elif trips_type == 'long':
            return self.get_long_trips(trips)
        else:
            return -1
    
    def get_particular_trips(self):
        for type_trips in self.types_trips:
            self.particular_trips[type_trips] = self.return_particular_trips_of_type(
                                                                self.trips, type_trips)
    
    def calculate_percentage_particular_trips(self, type_trips_numerator,
                                                type_trips_denominator = '', print_logs= True):
        
        if type_trips_denominator == '':
            trips_denominator = self.trips
        else:
            trips_denominator = self.particular_trips[type_trips_denominator]
        
        if trips_denominator.empty:
            # print("There is no trip with the type_trips_denominator specified")
            return None

        # We want the percentage of the numerator type of trips
        # in another group of trips (trips_denominator)
        trips_numerator = self.return_particular_trips_of_type(trips_denominator, type_trips_numerator)
        
        if not isinstance(trips_numerator, pd.DataFrame) and trips_numerator == -1:
            print("Invalid trip type for numerator")
            return None

        percentage = len(trips_numerator)/len(trips_denominator)

        if type_trips_denominator == '':
            if print_logs:
                print_message = 'The percentage of {type_trips_numerator} trips ' \
                                + '{period_covid} COVID is {percentage}'
                print(print_message.format(
                    type_trips_numerator = type_trips_numerator,
                    period_covid = self.period_covid,
                    percentage = percentage
                ))
            key_dictionary_percentage = type_trips_numerator
        else:
            if print_logs:
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
    
    def calculate_all_percentages(self, save = True, print_logs = True):
        self.get_particular_trips()

        type_trips_numerator = self.types_trips
        types_trips_denominator = self.types_trips + ['']

        for type_trips_numerator in type_trips_numerator:
            for type_trips_denominator in types_trips_denominator:
                # print(type_trips_numerator,type_trips_denominator)

                if type_trips_numerator != type_trips_denominator:
                    self.calculate_percentage_particular_trips(
                                    type_trips_numerator = type_trips_numerator,
                                    type_trips_denominator = type_trips_denominator,
                                    print_logs = False)

        if save:
            percentage_df = pd.DataFrame()
            percentage_df = percentage_df.append(
                        self.percentage,
                        ignore_index=True
                    )
            filename = 'particular_trips_percentage_{period_covid}_pandemic.csv'.format(
                                                                period_covid = self.period_covid)
            percentage_df.to_csv(self.destination_folder + filename, index = False)
    
    def calculate_monthly_percentage(self, trips = '', types_trips = '', print_logs = False):
        if trips == '':
            trips = self.trips
        if types_trips == '':
            types_trips = self.types_trips
        
        df_percentages = pd.DataFrame(dtype=object)

        for year in ['2018','2019','2020','2021','2022']:
            for month in range(1,13):
                trips_month = trips[year+'-'+str(month):year+'-'+ str(month)]
                if len(trips_month) > 0:
                    self.set_trips(trips_month)
                    self.calculate_all_percentages()

                    percentage = self.percentage
                    percentage['date'] = str(year) +'-'+str(month)
                    # print(percentage['date'])
                    df_percentages = df_percentages.append(
                        percentage,
                        ignore_index=True
                    )
        
        df_percentages = df_percentages.set_index('date')
        df_percentages.to_csv(self.destination_folder + 'particular_trips_monthly_percentage.csv', index=True)

    def plot_all_percentages(self):

        monthly_percentage = pd.read_csv(self.data_folder + 
            'trips/analysis_results/particular_trips_monthly_percentage.csv')
        dp = DataPreparation()
        monthly_percentage = dp.transform_to_datetime(monthly_percentage, ['date'])
        monthly_percentage = dp.transform_to_time_series(monthly_percentage, 'date', drop=True)
        monthly_percentage.head()

        for variable in list(monthly_percentage.columns):
            self.plot_percentage(monthly_percentage, variable)

    def plot_percentage(self, df, variable, phases = True, save = True):
        fig, ax = plt.subplots()
        fig.set_figwidth(20)
        fig.set_figheight(10)

        ax.plot(df.index, df.loc[:, variable], 'ro')
        ax.set_ylim(bottom = 0)

        if phases:
            ax.axvline(pd.to_datetime('2020-03-24'), color="black", linestyle="--", 
                        label='Início do lockdown em SP (2020-03-24)')
        
        # ax.xticks(fontsize = 20)

        # set monthly locator
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        # set formatter
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        # set font and rotation for date tick labels
        plt.gcf().autofmt_xdate()

        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        title = "Evolução das porcentagens de viagens da variável '{variable}'".format(variable = variable)
        ax.axes.set_title(title,fontsize=27, pad = 15)
        ax.set_xlabel('Date',fontsize=25, labelpad = 10)
        ax.set_ylabel('Percent of trips (%)',fontsize=25, labelpad = 10)
        
        plt.ylim(bottom=0)

        ax.legend(bbox_to_anchor=(0, 1), loc='upper left', fontsize=20)
        if save:
            filename = variable +'.png'
            plt.savefig(self.data_folder + 'charts/particular_trips/'+filename)
        plt.show()
      
    def plot_histogram_trip_duration(self, save = False, title = False):
        limit_bins_hours = 6
        limit_bins_seconds = 3600*limit_bins_hours+1
        step_seconds = 60*20
        variable = 'tripduration'

        # from 0 to 12 hours (3600*12 seconds), with step of 20 minutes
        bins = list(range(0,limit_bins_seconds,step_seconds))

        # fig, ax = plt.subplots()

        sns.set(rc={'figure.figsize':(20,11)})
        ax = sns.histplot(data=self.trips[variable], bins = bins, stat='percent')
        for i in ax.containers:
            ax.bar_label(i,fmt='%.1f', fontsize=25)
        
        # tickers for every 20 minutes
        ax.set_xticks(range(0,limit_bins_seconds,step_seconds), size = 20)
        figure(figsize=(12, 6), dpi=80)

        # show y axis labels in minutes, rather than in seconds

        ax.set_ylim(bottom = 0, top = 70)

        # ax.set(xlabel='Trip duration (min)', ylabel='Percent of trips (%)', fontsize=20)
        # ax.set(title='Trip duration distribution', fontsize=30)

        ax.axes.set_title('Trip duration variable distribution',fontsize=30, pad = 15)
        ax.set_xlabel('Trip duration (min)',fontsize=25, labelpad = 10)
        ax.set_ylabel('Percent of trips (%)',fontsize=25, labelpad = 10)

        ax.set_yticklabels(ax.get_yticks(), size=25)

        ax.set_xticklabels(ax.get_xticks(), size=25)

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: x//60))

        # ax.tick_params(labelsize=20)

        # if period != 'all' and day != '':
        # ax.set(title='Trip duration distribution ' + period + ' covid' + ' for ' + day)
        # else:
        #     ax.set(title='Trip duration distribution')
        # # plt.figure(figsize=(20,6))
        if save:
            ax.figure.savefig(self.data_folder + 'charts/histograms/tripduration_' +self.period_covid+'_covid.png', bbox_inches='tight')
    
    def plot_histogram(self, variable, save=False):
        if variable == 'tripduration':
            self.plot_histogram_trip_duration(save = save)
