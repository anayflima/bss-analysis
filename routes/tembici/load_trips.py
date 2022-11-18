import glob
import pandas as pd
import sys
import tembici.stations as st

sys.path.append("..")

from bikescience import load_trips as tr

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
    tr.create_time_features(trips)

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

def select_distance_range(trips,distance_range,stations,stations_distances):
    
    trips_filter = st.merge_trips_and_stations(trips, stations)
    trips_filter = st.merge_trips_stations_and_distances(trips_filter, stations_distances)
    distance_min = distance_range[0]
    distance_max = distance_range[1]
    trips_filter = trips_filter[(trips_filter['distance'] >= distance_min) & (trips_filter['distance'] <= distance_max)]
    
    return trips_filter

def select_duration_range(trips,duration_range):
    trips = trips[~trips['tripduration'].isnull()]
    duration_min = duration_range[0]*60
    duration_max = duration_range[1]*60
    if duration_range[1] < 90:
        trips = trips[(trips['tripduration'] >= duration_min) & (trips['tripduration'] <= duration_max)]
    else:
        trips = trips[(trips['tripduration'] >= duration_min)]
    return trips

def select_duration_range_min_max(trips,min,max):
    trips = trips[~trips['tripduration'].isnull()]
    duration_min = min*60
    duration_max = max*60
    trips = trips[(trips['tripduration'] >= duration_min) & (trips['tripduration'] <= duration_max)]
    return trips
