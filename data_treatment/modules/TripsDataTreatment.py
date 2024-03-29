import pandas as pd
import glob
import os
import sys
sys.path.append('./data_treatment')
from modules.DataTreatment import DataTreatment

class TripsDataTreatment(DataTreatment):
    def transform_xlsx_to_csv_and_copy_to_destination_folder(self):
        if self.filename == '':
            filename = '*.xlsx'
        else:
            filename = self.filename + '.xlsx'
        
        # print(self.source_folder_path + filename)

        for f in glob.glob(self.source_folder_path + filename):

            last_dot = f.rindex('.')
            file_name = f[:last_dot]

            file_name = file_name.split('/')[-1]
            
            # this line is specific to trips data
            xls = pd.read_excel(f, usecols='B:F')

            file_path = self.destination_folder_path + file_name + '.csv'
            
            xls.to_csv(file_path,encoding='utf-8',index=False)

    def fix_column_names(self, df):
        if 'start_time' in df.columns:
            df.rename(columns={'start_time': 'start_date'}, inplace=True)
        if 'end_time' in df.columns:
            df.rename(columns={'end_time': 'end_date'}, inplace=True)
        if 'initial_station_name' in df.columns:
            df.rename(columns={'initial_station_name': 'start_station_name'}, inplace=True)
        if 'final_station_name' in df.columns:
            df.rename(columns={'final_station_name': 'end_station_name'}, inplace=True)
        # for columns in spanish (new data of 2022)
        if 'id_recorrido' in df.columns:
            df.rename(columns={'id_recorrido': 'trip_id'}, inplace=True)
        if 'duracion_recorrido' in df.columns:
            df.rename(columns={'duracion_recorrido': 'duration_seconds'}, inplace=True)
        if 'nombre_estacion_origen' in df.columns:
            df.rename(columns={'nombre_estacion_origen': 'start_station_name'}, inplace=True)
        if 'fecha_origen_recorrido' in df.columns:
            df.rename(columns={'fecha_origen_recorrido': 'start_date'}, inplace=True)
        if 'fecha_destino_recorrido' in df.columns:
            df.rename(columns={'fecha_destino_recorrido': 'end_date'}, inplace=True)
        if 'nombre_estacion_destino' in df.columns:
            df.rename(columns={'nombre_estacion_destino': 'end_station_name'}, inplace=True)
        if 'lat_estacion_origen' in df.columns:
            df.rename(columns={'lat_estacion_origen': 'initial_station_latitude'}, inplace=True)
        if 'long_estacion_origen' in df.columns:
            df.rename(columns={'long_estacion_origen': 'initial_station_longitude'}, inplace=True)
        if 'lat_estacion_destino' in df.columns:
            df.rename(columns={'lat_estacion_destino': 'final_station_latitude'}, inplace=True)
        if 'long_estacion_destino' in df.columns:
            df.rename(columns={'long_estacion_destino': 'final_station_longitude'}, inplace=True)
        if 'id_estacion_origen' in df.columns:
            df.rename(columns={'id_estacion_origen': 'start_station_id'}, inplace=True)
        if 'id_estacion_destino' in df.columns:
            df.rename(columns={'id_estacion_destino': 'end_station_id'}, inplace=True)
        
    
    def padronize_dfs(self):
        '''
            Considere that all the data is already in the destination
            folder and in csv format.
            Fix accents and padronize columns names
        '''
        if self.filename == '':
            filename = '*.csv'
        else:
            filename = self.filename + '.csv'
        
        for f in glob.glob(self.destination_folder_path + filename):
            # print(f)
            def fix_accents_names():
                df = pd.read_csv(f)
                self.fix_column_names(df)
                df.start_station_name = df.start_station_name.dropna().apply(self.fix_accents)
                df.end_station_name = df.end_station_name.dropna().apply(self.fix_accents)
                
                start = df.start_station_name.unique()
                start.sort()

                end = df.end_station_name.unique()
                end = [i for i in end if not isinstance(i, float)]
                end.sort()

                # assert all(start == end) #PERGUNTAR

                df.to_csv(f, index=False)
            
            try:
                fix_accents_names()
            except:
                with open(f, encoding = 'iso8859-1') as file:
                    data = file.read().replace("�", "?")
                with open(f, 'w') as file:
                    file.write(data)
                fix_accents_names()

        
    def padronize_filenames(self):
        '''
        Padronize file names to start with trips_BikeSampa_YYYY-MM.csv
        Code specific for the data given by tembici
        '''

        incorrect_files_date = ['20210401', '20210501', '20210601', '20210701', '20210801', '20210901']

        for date in incorrect_files_date:
            filename = 'trips_BikeSampa_' + date + '.csv'
            if (os.path.isfile(self.destination_folder_path + filename)):
                correct_date = date[:4] + '-' + date[4:6] + '-' + date[6:8]
                corrected_filename = 'trips_BikeSampa_' + correct_date +'.csv'
                os.rename(self.destination_folder_path + filename,
                        self.destination_folder_path + corrected_filename)
    
    def treat_trips_data(self):
        '''
            In order to complete all trips data treatment process,
            we need to:
            1 - Transform all to csv and copy to destination folder
            2 - Padronize data frames, fixing accents and column names
            3 - Padronize filenames
        '''

        print('Transforming xlsx to csv')
        self.transform_xlsx_to_csv_and_copy_to_destination_folder()

        print('Copying csv files to destination folder')
        self.copy_csv_to_destination_folder()

        print('Fixing accents and column names')
        self.padronize_dfs()

        print('Padronizing filenames')
        self.padronize_filenames()

