import glob
import pandas as pd
import sys
import holidays

sys.path.append("..")

years = range(2018, 2022)
sp_holidays = holidays.BR(state='SP', years=years)
sp_holidays = [pd.Period(freq='d', year=d.year, month=d.month, day=d.day)
                for d in sp_holidays]

def create_time_features(trips):
    """
    ** Internal use function **
    
    Preparation of the trips dataframe.
    """

    trips['starttime'] = pd.to_datetime(trips['starttime'])
    trips['per_day'] = trips['starttime'].dt.to_period('d')
    trips['hour'] = trips['starttime'].dt.hour
    trips['week_day'] = trips['starttime'].dt.weekday
    trips['weekend'] = trips['week_day'] >= 5
    trips['holiday'] = trips['per_day'].isin(sp_holidays)

def remove_timezone(row):
    return row.tz_localize(None)

def load_trips_files(file_filter, show=False):
    print('load_trips_files')
    trip_files = glob.glob(file_filter)
    df_list = []
    for f in trip_files:
        if show:
            print(f)
        df = pd.read_csv(f, parse_dates=['start_date', 'end_date'])
        # df = pd.read_csv(f,)
        df_list.append(df.drop_duplicates())
    
    trips = pd.concat(df_list,sort=False)
    trips.rename(columns={
                    'start_date': 'starttime', 
                    'end_date': 'stoptime', 
                    'ano_nasc': 'birth year',
                    'user_type': 'usertype',
                    'duration_seconds': 'tripduration',
                 }, inplace=True)

    # CHANGEE

    trips['starttime'] = trips['starttime'].apply(remove_timezone)
    trips['stoptime'] = trips['stoptime'].apply(remove_timezone)
    create_time_features(trips)

    trips.insert(0, 'Index', range(0,0 + len(trips)))
    trips = trips.reset_index(drop=True)
    trips = trips.set_index('Index')

    trips['starttime'] = trips['starttime'].apply(remove_timezone)
    return trips

def women(trips):
    """Filter trips rode by women, returning a new dataframe."""
    return trips[trips['gender'] == 'Fem']

def men(trips):
    """Filter trips rode by men, returning a new dataframe."""
    return trips[trips['gender'] == 'Masc']

gender_functions = [lambda trips: trips, women, men]

def select_age_range(trips,age_range):
    trips = trips[~trips['birth year'].isnull()]
    trips = trips[(trips['starttime'].dt.year - trips['birth year'] >= age_range[0]) & (trips['starttime'].dt.year - trips['birth year'] <= age_range[1])]
    return trips