import re
import pandas as pd
import os
import sys
sys.path.append('./stations_treatment')
sys.path.append('./stations_treatment/modules/')
sys.path.append('../../')
sys.path.append('../')
import os

class TripStationsTreatment:
    def __init__(self):
        pass
    
    def find_individual_station_id(self, text):
        text = str(text)
        split = text.split('-')
        for portion in split:
            portion = portion.strip()
            if re.search("^[0-9]+$", portion):
                return int(portion)
    
    def find_stations_id_and_save_csv(self, filename):
        '''
            filename has to be passed with an extension (.csv)
        '''

        trips = pd.read_csv(filename)
        start_station_id = trips['start_station_name'].apply(self.find_individual_station_id)

        index = trips.columns.get_loc('start_station_name') + 1
        trips.insert(index, 'start_station_id',start_station_id)

        end_station_id = trips['end_station_name'].apply(self.find_individual_station_id)

        index = trips.columns.get_loc('end_station_name') + 1
        trips.insert(index, 'end_station_id',end_station_id)

        trips.to_csv(filename, index=False)
        return trips
    
    def find_station_ids_and_add_columns(self, trips):
        start_station_id = trips['start_station_name'].apply(self.find_individual_station_id)

        index = trips.columns.get_loc('start_station_name') + 1
        trips.insert(index, 'start_station_id',start_station_id)

        end_station_id = trips['end_station_name'].apply(self.find_individual_station_id)

        index = trips.columns.get_loc('end_station_name') + 1
        trips.insert(index, 'end_station_id',end_station_id)

        return trips
    
    def find_station_names_and_add_columns(self, trips, stations_file_path = './data/stations/treated_data/2021.11.08_Endereços-BikeSAMPA.csv'):
        stations = pd.read_csv(stations_file_path)
        stations_name = stations[['id', 'name']]
        merge = trips.merge(stations_name, how = 'left', left_on=['start_station_id'],
                    right_on=['id'])

        merge = merge.drop(['id'], axis = 1)

        merge = merge.rename(columns={'start_station_name': 'start_station_name_old',
                                        'name': 'start_station_name'})

        merge = merge.merge(stations_name, how = 'left', left_on=['end_station_id'],
                            right_on=['id'])

        merge = merge.drop(['id'], axis = 1)

        merge = merge.rename(columns={'end_station_name': 'end_station_name_old',
                                        'name': 'end_station_name'})

        return merge