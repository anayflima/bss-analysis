import time
import sys
sys.path.append('./data_treatment')
import os
from modules.StationsDataTreatment import StationsDataTreatment

start = time.time()

if 'data_treatment' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'stations/original_data/'
destination_folder_path = data_folder + 'stations/treated_data/'

dt = StationsDataTreatment(source_folder_path, destination_folder_path)
dt.transform_xlsx_to_csv_and_copy_to_destination_folder()