import pandas as pd

class DataPreparation():
    def remove_timezone(self, row):
        return row.tz_localize(None)

    def transform_to_datetime(self, df, columns):
        for column in columns:
            df[column] = pd.to_datetime(df[column])
            df[column] = df[column].apply(self.remove_timezone)
        return df
    
    def transform_to_time_series(self, df, index_column, drop = False):
        df.set_index(pd.DatetimeIndex(df[index_column].dt.date),
                        inplace=True, drop = drop)
        if drop and index_column in df.columns:
            df = df.drop(index_column, axis=1)
        df = df.sort_index()
        df = df.rename_axis('date')
        return df
    
    def calculate_and_add_age_column(self, df):
        df['birth_year'] = pd.to_datetime(df['birth_year'], errors='coerce', format='%Y')
        df['age'] = df["starttime"].dt.year - df["birth_year"].dt.year
        # To avoid warning message from python: 
        # "A value is trying to be set on a copy of a slice from a DataFrame"
        pd.options.mode.chained_assignment = None  # default='warn'

        df['age'][(df['age'] < 0) | (df['age'] > 100) ] = None
        return df