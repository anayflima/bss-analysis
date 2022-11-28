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
    
    def to_datetime(self, row):
        try:
            row = float(row)
            output = pd.to_datetime(row, format='%Y')
        except:
            try:
                output = pd.to_datetime(row)
            except:
                # print(row)
                output = None
        return output
    
    def calculate_and_add_age_column(self, df):
        # print('birth_year that could not be transformed')
        df['birth_year'] = df['birth_year'].apply(self.to_datetime)
        df['age'] = df["starttime"].dt.year - df["birth_year"].dt.year

        df['age'][(df['age'] < 0) | (df['age'] > 100) ] = None
        # print(df['age'])
        return df