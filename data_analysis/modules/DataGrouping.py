import pandas as pd
import numpy as np

class DataGrouping():
    def __init__(self, df):
        self.df = df
    
    def find_daily_average(self, variable):
        '''
        In order to find the daily average, you need to consider only non-null values
        '''
        grouped_df = self.df[variable].groupby(pd.Grouper(freq='D')).mean()
        grouped_df = pd.DataFrame(grouped_df, columns=[variable])
        return grouped_df

    def first_daily_value(self, variable):
        '''
            Some variables are dependent only on the day,
            so they will be same for every trip on the same day
        '''
        grouped_df = self.df[variable].groupby(pd.Grouper(freq='D')).first()
        grouped_df = pd.DataFrame(grouped_df, columns=[variable])
        return grouped_df
    
    def find_number_daily_occurrences(self, column_name_count = 'number_of_trips',
                                variable_count = 'starttime'):
        '''
            Returns data frame with number of trips in each day
        '''
        daily_trips_number = self.df[variable_count].groupby(pd.Grouper(freq='D')).count()
        grouped_df = pd.DataFrame(daily_trips_number)
        grouped_df = grouped_df.rename(columns={variable_count: column_name_count})
        return grouped_df
    
    def find_number_occurrences_given_freq(self, freq = 'MS',
                                column_name_count = 'number_of_trips',
                                variable_count = 'starttime'):
        '''
            Returns data frame with number of trips in each day
        '''
        daily_trips_number = self.df[variable_count].groupby(pd.Grouper(freq=freq)).count()
        grouped_df = pd.DataFrame(daily_trips_number)
        grouped_df = grouped_df.rename(columns={variable_count: column_name_count})
        return grouped_df
    
    def group_by_given_freq(self, freq = 'MS', column_name_count = 'number_of_trips',
                            variable_count = 'starttime', covid = False):
        if covid:
            output_df = self.df.filter(['date'])
        else:
            output_df = self.find_number_occurrences_given_freq(freq, column_name_count,
                                                            variable_count)
        mean_df = self.df.groupby(pd.Grouper(freq=freq)).mean()
        std_df = self.df.groupby(pd.Grouper(freq=freq)).std()
        mean_df = pd.merge(output_df, mean_df, left_index=True, right_index=True)
        std_df = pd.merge(output_df, std_df, left_index=True, right_index=True)
        return mean_df, std_df

    def group_all_trips_data(self):
        output_df = self.find_number_daily_occurrences()

        for variable in ['tripduration', 'hour', 'age', 'distance']:
            variable_df = self.find_daily_average(variable)
            output_df = pd.merge(output_df, variable_df, left_index=True, right_index=True)

        for variable in ['week_day', 'weekend', 'holiday']:
            variable_df = self.first_daily_value(variable)
            output_df = pd.merge(output_df, variable_df, left_index=True, right_index=True)

        return output_df
    