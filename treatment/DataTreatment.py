import pandas as pd
import glob
import shutil
import os
import time

class DataTreatment:
    def __init__(self, source_folder_path, destination_folder_path, filename = ''):
        '''
            filename: regex of files that should be treated, without extension
        '''
        self.filename = filename
        self.source_folder_path = source_folder_path
        self.destination_folder_path = destination_folder_path

    def transform_xlsx_to_csv_and_copy_to_destination_folder(self):
        if self.filename == '':
            filename = '*.xlsx'
        else:
            filename = self.filename + '.xlsx'
        
        print(self.source_folder_path + filename)

        for f in glob.glob(self.source_folder_path + filename):

            last_dot = f.rindex('.')
            file_name = f[:last_dot]

            file_name = file_name.split('/')[-1]

            xls = pd.read_excel(f, usecols='B:F')

            file_path = self.destination_folder_path + file_name + '.csv'
            
            xls.to_csv(file_path,encoding='utf-8',index=False)
    
    def copy_csv_to_destination_folder(self):
        if self.filename == '':
            filename = '*.csv'
        else:
            filename = self.filename + '.csv'
        
        for f in glob.glob(self.source_folder_path + filename):
            file_name = str(f).split('/')[-1]
            print(file_name)

            destination_file_path = self.destination_folder_path + file_name

            shutil.copyfile(f, destination_file_path)

    def fix_accents(self, text):
        try:
            return bytes(text, 'iso-8859-1').decode('utf-8')
        except UnicodeDecodeError:
            return text
        except TypeError:
            return text
    
    def fix_column_names(self, df, trips = True):
        if trips:
            if 'start_time' in df.columns:
                df.rename(columns={'start_time': 'start_date'}, inplace=True)
            if 'end_time' in df.columns:
                df.rename(columns={'end_time': 'end_date'}, inplace=True)
            if 'initial_station_name' in df.columns:
                df.rename(columns={'initial_station_name': 'start_station_name'}, inplace=True)
            if 'final_station_name' in df.columns:
                df.rename(columns={'final_station_name': 'end_station_name'}, inplace=True)
        else:
            if 'LATITUDE (SIG 4326)' in df.columns:
                df.rename(columns={'LATITUDE (SIG 4326)': 'lat'}, inplace=True)
            if 'LONGITUDE (SIG 4326)' in df.columns:
                df.rename(columns={'LONGITUDE (SIG 4326)': 'lon'}, inplace=True)
    
    def padronize_dfs(self, trips = True):
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
            print(f)

            if trips:
                def fix_accents_names():
                    df = pd.read_csv(f)
                    self.fix_column_names(df, trips)
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
            else:
                df = pd.read_csv(f)
                self.fix_column_names(df, trips)
                df.to_csv(f, index=False)

        
    def padronize_filenames(self):
        '''
        Padronize file names to start with trips_BikeSampa_YYYY-MM.csv
        Code specific for the data given by tembici
        '''

        incorrect_files_date = ['20210401', '20210501', '20210601', '20210701', '20210801', '20210901']

        for date in incorrect_files_date:
            filename = 'trips_BikeSampa_' + date + '.csv'
            if (os.path.exists(filename)):
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
        start = time.time()

        print('Transforming xlsx to csv')
        self.transform_xlsx_to_csv_and_copy_to_destination_folder()

        print('Copying csv files to destination folder')
        self.copy_csv_to_destination_folder()

        print('Fixing accents and column names')
        self.padronize_dfs()

        print('Padronizing filenames')
        self.padronize_filenames()

        end = time.time()

        print('Time to complete trip data treatment: {time}'.format(time = end - start))

