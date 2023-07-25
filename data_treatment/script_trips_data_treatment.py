import time
import sys
sys.path.append('./data_treatment')
import os
from modules.TripsDataTreatment import TripsDataTreatment

start = time.time()

if 'data_treatment' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'trips/original_data/'
destination_folder_path = data_folder + 'trips/treated_data/'

'''
To treat only files that follow a specific name pattern:
'''
# filename = 'trips_BikeSampa_2022-*'
# dt = TripsDataTreatment(source_folder_path, destination_folder_path, filename)

'''
To treat all files in the folder:
'''
dt = TripsDataTreatment(source_folder_path, destination_folder_path)

dt.treat_trips_data()
print('DataTreatment completed')

end = time.time()

print('Time to complete trip data treatment: {time}'.format(time = end - start))