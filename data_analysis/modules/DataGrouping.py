import pandas as pd

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
    
    def find_number_daily_occurrences(self):
        '''
            Returns data frame with number of trips in each day
        '''
        variable = 'starttime'
        daily_trips_number = self.df[variable].groupby(pd.Grouper(freq='D')).count()
        grouped_df = pd.DataFrame(daily_trips_number)
        grouped_df = grouped_df.rename(columns={variable: 'number_of_trips'})
        return grouped_df
    
    def group_all_trips_data(self):
        output_df = self.find_number_daily_occurrences()

        for variable in ['tripduration', 'hour', 'age']:
            variable_df = self.find_daily_average(variable)
            output_df = pd.merge(output_df, variable_df, left_index=True, right_index=True)

        for variable in ['week_day', 'weekend', 'holiday']:
            variable_df = self.first_daily_value(variable)
            output_df = pd.merge(output_df, variable_df, left_index=True, right_index=True)

        return output_df