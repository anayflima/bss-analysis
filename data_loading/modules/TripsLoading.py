import glob
import pandas as pd
import holidays
import numpy as np
from datetime import datetime
import os

# to import the env variables:
from dotenv import load_dotenv
load_dotenv()

class TripsLoading():
    def __init__(self):
        last_year = datetime.strptime(os.environ['LAST_DAY_TRIPS'], '%Y-%m-%d').year
        years = range(2018, last_year + 1)
        sp_holidays = holidays.BR(state='SP', years=years)
        sp_holidays = [pd.Period(freq='d', year=d.year, month=d.month, day=d.day)
                        for d in sp_holidays]
        self.sp_holidays = sp_holidays
    
    def convert_to_datetime(self, date):
        if '/' in date:
            date_transformed = pd.to_datetime(date, format='%d/%m/%Y %H:%M')
        else:
            date_transformed = pd.to_datetime(date, format='%Y-%m-%d %H:%M')
        return date_transformed
    
    def create_time_features(self, trips):
        """
        ** Internal use function **

        Preparation of the trips dataframe.
        """

        trips['per_day'] = trips['starttime'].dt.to_period('d')
        trips['hour'] = trips['starttime'].dt.hour
        trips['week_day'] = trips['starttime'].dt.weekday
        trips['weekend'] = trips['week_day'] >= 5
        trips['holiday'] = trips['per_day'].isin(self.sp_holidays)
    
    def remove_timezone(self, row):
        return row.tz_localize(None)
    
    def delete_unnecessary_columns(self, trips):
        trips = trips.drop(['trip_id',
                            'initial_station_latitude',
                            'initial_station_longitude',
                            'final_station_latitude',
                            'final_station_longitude',
                            'direccion_estacion_origen',
                            'direccion_estacion_destino',
                            'id_usuario',
                            'modelo_bicicleta'], axis = 1, errors = 'ignore')
        return trips

    def load_trips_files(self, file_filter, show=False):
        trip_files = glob.glob(file_filter)
        df_list = []
        for f in trip_files:
            if show:
                print(f)
            df = pd.read_csv(f)
            df_list.append(df.drop_duplicates())
        
        trips = pd.concat(df_list,sort=False)
        trips.rename(columns={
                        'start_date': 'starttime', 
                        'end_date': 'stoptime', 
                        'ano_nasc': 'birth_year',
                        'user_type': 'usertype',
                        'duration_seconds': 'tripduration',
                    }, inplace=True)
        
        trips['starttime'] = trips['starttime'].apply(self.convert_to_datetime)
        trips['starttime'] = trips['starttime'].apply(self.remove_timezone)
        trips['stoptime'] = trips['stoptime'].apply(self.convert_to_datetime)
        trips['stoptime'] = trips['stoptime'].apply(self.remove_timezone)

        if 'birth_year' not in trips.columns:
            trips["birth_year"] = np.nan
        
        self.calculate_and_add_age_column(trips)

        self.create_time_features(trips)

        trips = self.delete_unnecessary_columns(trips)

        trips.insert(0, 'Index', range(0,0 + len(trips)))
        trips = trips.reset_index(drop=True)
        trips = trips.set_index('Index')

        return trips
    
    def calculate_and_add_age_column(self, df):
        df['birth_year'] = df['birth_year'].apply(self.to_datetime)
        df['age'] = df["starttime"].dt.year - df["birth_year"].dt.year
        df.loc[(df['age'] < 0) | (df['age'] > 100), 'age'] = None
        return df
    
    def to_datetime(self, row):
        try:
            row = float(row)
            output = pd.to_datetime(row, format='%Y')
        except:
            try:
                output = pd.to_datetime(row)
            except:
                output = None
        return output
    
    def select_age_range(self, trips, age_range):
        trips = trips[~trips['birth_year'].isnull()]
        trips = trips[(trips['starttime'].dt.year - trips['birth_year'] >= age_range[0])
                    & (trips['starttime'].dt.year - trips['birth_year'] <= age_range[1])]
        return trips
