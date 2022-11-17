import pandas as pd

import os
import sys
sys.path.append('./stations_treatment')
sys.path.append('../')

if 'stations_treatment' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

stations = pd.read_csv(data_folder + 'stations/original_data/2021.11.08_Endereços-BikeSAMPA.csv')
stations = stations.rename(columns={'NÚMERO ESTAÇÃO':'id',
                                    'NOME':'name',
                                    'ENDEREÇO ':'address',
                                    'LATITUDE (SIG 4326)':'lat',
                                    'LONGITUDE (SIG 4326)':'lon'})
                                
from modules.GeolocatorTomTom import *
import json

tomTomKey="gKJbocBwXPikRmcqAH42lchEFHAHhA3d"

def getCoordinates(location):
    geolocator = GeolocatorTomTom(tomTomKey)
    latitude, longitude = geolocator.getCoordinates(location)
    return (latitude,longitude)

latitude, longitude = getCoordinates("Rua Lourenço de Almeida, 36")
stations['lat'][28] = latitude
stations['lon'][28] = longitude

latitude, longitude = getCoordinates("Rua Artur Etzel")
stations['lat'][37] = latitude
stations['lon'][37] = longitude

latitude, longitude = getCoordinates("Rua Cravinhos, 136")
stations['lat'][58] = latitude
stations['lon'][58] = longitude

def convert_to_float(row):
    string_row = str(row)
    string_row = string_row.replace("'", "")
    return float(string_row)

stations['lat'] = stations['lat'].apply(convert_to_float)
stations['lon'] = stations['lon'].apply(convert_to_float)

stations.to_csv(data_folder + 'stations/treated_data/2021.11.08_Endereços-BikeSAMPA.csv')