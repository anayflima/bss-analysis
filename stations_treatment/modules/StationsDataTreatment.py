import re
import pandas as pd
import os


import sys
sys.path.append('../modules')
sys.path.append('./stations_treatment/modules')

class StationsDataTreatment:
    def __init__(self):
        pass
    
    def find_individual_station_id(self, text):
        text = str(text)
        split = text.split('-')
        for portion in split:
            portion = portion.strip()
            # print(portion)
            if re.search("^[0-9]+$", portion):
                # print('é só número (id)')
                return portion
    
    def find_stations_id(self, filename):
        '''
            filename has to be passed with an extension (.csv)
        '''
        # TODO: this should be done in the load_trips method

        trips = pd.read_csv(filename)
        start_station_id = trips['start_station_name'].apply(self.find_individual_station_id)

        index = trips.columns.get_loc('start_station_name') + 1
        trips.insert(index, 'start_station_id',start_station_id)

        end_station_id = trips['end_station_name'].apply(self.find_individual_station_id)

        index = trips.columns.get_loc('end_station_name') + 1
        trips.insert(index, 'end_station_id',end_station_id)

        trips.to_csv(filename, index=False)
        return trips