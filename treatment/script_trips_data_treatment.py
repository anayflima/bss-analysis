from modules.TripsDataTreatment import TripsDataTreatment

source_folder_path = './data/trips/test/original_data/'
destination_folder_path = './data/trips/test/treated_data/'

'''
To treat only files that follow a specific name pattern:
'''
# filename = 'trips_BikeSampa_2020-*'
# dt = DataTreatment(source_folder_path, destination_folder_path, filename)

dt = TripsDataTreatment(source_folder_path, destination_folder_path)
dt.treat_trips_data()
print('DataTreatment completed')