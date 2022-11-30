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